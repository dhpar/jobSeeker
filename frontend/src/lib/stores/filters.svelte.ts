import { defaultFilters, type JobFilters } from '../api/filters'

let filters = $state<JobFilters>({ ...defaultFilters })

export function getFilters(): JobFilters {
  return filters
}

export function setFilter<K extends keyof JobFilters>(key: K, value: JobFilters[K]): void {
  filters = { ...filters, [key]: value }
}

export function toggleSource(source: string): void {
  const has = filters.sources.includes(source)
  filters = {
    ...filters,
    sources: has ? filters.sources.filter((s) => s !== source) : [...filters.sources, source],
  }
}

export function resetFilters(): void {
  filters = { ...defaultFilters }
}

export function parseCsv(value: string): string[] {
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}
