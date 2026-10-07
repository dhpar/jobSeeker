export const scrapeState = $state({
  running: false,
  connected: false,
  error: null as string | null,
})

export function scrapeStarted(): void {
  scrapeState.running = true
  scrapeState.error = null
}

export function scrapeFinished(ok: boolean, error?: string): void {
  scrapeState.running = false
  scrapeState.error = ok ? null : (error ?? 'Scrape failed')
}
