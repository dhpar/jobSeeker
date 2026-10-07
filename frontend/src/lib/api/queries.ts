import { createMutation, createQuery, queryOptions, useQueryClient } from '@tanstack/svelte-query'
import { scrapeFinished, scrapeStarted, scrapeState } from '../stores/scrape.svelte'
import { apiGet } from './client'
import type { JobsResponse, ScrapeResponse } from './types'

export const jobKeys = {
  all: ['jobs'] as const,
  list: () => [...jobKeys.all, 'list'] as const,
}

export const jobsQueryOptions = queryOptions({
  queryKey: jobKeys.list(),
  queryFn: () => apiGet<JobsResponse>('/jobs'),
  staleTime: 60_000,
})

export function useJobsQuery() {
  return createQuery(() => jobsQueryOptions)
}

export function useScrapeMutation() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: () => apiGet<ScrapeResponse>('/scrape'),
    onSuccess: () => {
      scrapeStarted()
      // Fallback when the live socket is down: refresh once the crawl should be done.
      // The normal path is the /ws scrape_completed event.
      if (!scrapeState.connected) {
        window.setTimeout(() => {
          scrapeFinished(true)
          queryClient.invalidateQueries({ queryKey: jobKeys.all })
        }, 20_000)
      }
    },
    onError: (error) => scrapeFinished(false, error.message),
  }))
}
