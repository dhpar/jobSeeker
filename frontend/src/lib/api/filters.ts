export interface JobFilters {
  /** free-text search across title, company, location, and JD text */
  query: string
  /** keep only these sources (empty = all) */
  sources: string[]
  /** comma-separated keywords; all must appear in the JD text */
  keywords: string[]
  /** JD must contain at least one of these (OR semantics) */
  anyKeywords: string[]
  remoteOnly: boolean
}

export const defaultFilters: JobFilters = {
  query: '',
  sources: [],
  keywords: [],
  anyKeywords: [],
  remoteOnly: false,
}
