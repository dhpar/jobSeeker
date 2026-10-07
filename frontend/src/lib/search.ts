import type { Job } from './api/types'
import type { JobFilters } from './api/filters'

function includesIgnoreCase(haystack: string, needle: string): boolean {
  return haystack.toLowerCase().includes(needle.toLowerCase())
}

function matchesFreeText(job: Job, query: string): boolean {
  if (!query.trim()) return true
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean)
  const haystack = `${job.title} ${job.company} ${job.location} ${job.text}`.toLowerCase()
  return terms.every((t) => haystack.includes(t))
}

function matchesKeywords(job: Job, keywords: string[]): boolean {
  const text = job.text.toLowerCase()
  return keywords.every((k) => k && text.includes(k.toLowerCase()))
}

function matchesAnyKeywords(job: Job, keywords: string[]): boolean {
  if (keywords.length === 0) return true
  const text = job.text.toLowerCase()
  return keywords.some((k) => k && text.includes(k.toLowerCase()))
}

function matchesRemote(job: Job, remoteOnly: boolean): boolean {
  if (!remoteOnly) return true
  return includesIgnoreCase(job.location, 'remote')
}

export function filterJobs(jobs: Job[], filters: JobFilters): Job[] {
  return jobs.filter((job) => {
    if (filters.sources.length > 0 && !filters.sources.includes(job.source)) return false
    if (!matchesFreeText(job, filters.query)) return false
    if (!matchesKeywords(job, filters.keywords)) return false
    if (!matchesAnyKeywords(job, filters.anyKeywords)) return false
    if (!matchesRemote(job, filters.remoteOnly)) return false
    return true
  })
}
