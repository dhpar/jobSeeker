import type { QueryClient } from '@tanstack/svelte-query'
import { scrapeFinished, scrapeStarted, scrapeState } from '../stores/scrape.svelte'
import { jobKeys } from './queries'
import type { ScrapeEventMessage } from './types'

const MAX_RETRY_DELAY_MS = 15_000

/**
 * Connect to the backend /ws scrape-progress socket.
 * Returns a cleanup function that closes the socket and stops reconnecting.
 */
export function connectScrapeSocket(queryClient: QueryClient): () => void {
  let socket: WebSocket | null = null
  let disposed = false
  let attempts = 0

  const handleMessage = (message: ScrapeEventMessage) => {
    if (message.event === 'scrape_started') {
      scrapeStarted()
    } else if (message.event === 'scrape_completed') {
      const ok = message.ok ?? false
      scrapeFinished(ok, message.error)
      if (ok) {
        queryClient.invalidateQueries({ queryKey: jobKeys.all })
      } else {
        console.error('Scrape failed:', message.error)
      }
    }
  }

  const connect = () => {
    if (disposed) return
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    socket = new WebSocket(`${protocol}://${window.location.host}/ws`)

    socket.onopen = () => {
      attempts = 0
      scrapeState.connected = true
    }

    socket.onmessage = (event) => {
      try {
        handleMessage(JSON.parse(event.data) as ScrapeEventMessage);
      } catch (error) {
        console.error('Failed to parse scrape event message', error);
      }
    }

    socket.onclose = () => {
      scrapeState.connected = false;
      if (disposed) return;
      const delay = Math.min(1000 * 2 ** attempts, MAX_RETRY_DELAY_MS);
      attempts += 1;
      window.setTimeout(connect, delay);
    }
  }

  connect()

  return () => {
    disposed = true
    socket?.close()
  }
}
