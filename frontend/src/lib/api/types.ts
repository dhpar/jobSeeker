export type JobSource = 'greenhouse' | 'lever' | 'ashby' | 'hn'

export interface Job {
  source: JobSource | string
  company: string
  title: string
  location: string
  url: string
  text: string
}

export interface JobsResponse {
  data: Job[]
}

export interface ScrapeResponse {
  status: string
}

export interface ScrapeEventMessage {
  event: 'scrape_started' | 'scrape_completed'
  ok?: boolean
  error?: string
}

export interface HealthResponse {
  message: string
  docs: string
}
