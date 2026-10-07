import { createMutation, createQuery, queryOptions, useQueryClient } from '@tanstack/svelte-query'
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
    onSuccess: () => queryClient.invalidateQueries({ queryKey: jobKeys.all }),
  }))
}
