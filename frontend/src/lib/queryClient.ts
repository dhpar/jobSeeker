import { QueryClient } from '@tanstack/svelte-query'

export function createQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: 2,
        refetchOnWindowFocus: false,
        staleTime: 60_000,
      },
    },
  })
}
