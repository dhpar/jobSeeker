<script module lang="ts">
  export const navItems: { id: TRoute; label: string }[] = [
    { id: 'jobs', label: 'Jobs' },
    { id: 'resume', label: 'Resume' },
    { id: 'ai-search', label: 'AI Search' },
  ]
</script>

<script lang="ts">
  import { QueryClientProvider } from '@tanstack/svelte-query'
  import { onMount } from 'svelte'
  import JobsPage from './lib/components/JobsPage.svelte'
  import ResumePage from './lib/components/ResumePage.svelte'
  import AiSearchPage from './lib/components/AiSearchPage.svelte'
  import { createQueryClient } from './lib/queryClient'
  import { connectScrapeSocket } from './lib/api/ws'
  import { route, type TRoute } from './lib/components/Header.svelte'

  const queryClient = createQueryClient()

  onMount(() => connectScrapeSocket(queryClient))
  let page: TRoute = route.page;
</script>

<QueryClientProvider client={queryClient}>
  {#if page === 'jobs'}
    <JobsPage />
  {:else if page === 'resume'}
    <ResumePage />
  {:else if page === 'ai-search'}
    <AiSearchPage />
  {/if}
</QueryClientProvider>
