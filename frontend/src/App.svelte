<script lang="ts">
  import { QueryClientProvider } from '@tanstack/svelte-query'
  import JobsPage from './lib/components/JobsPage.svelte'
  import ResumePage from './lib/components/ResumePage.svelte'
  import AiSearchPage from './lib/components/AiSearchPage.svelte'
  import { createQueryClient } from './lib/queryClient'

  const queryClient = createQueryClient()

  type Route = 'jobs' | 'resume' | 'ai-search'
  let route = $state<Route>('jobs')

  const navItems: { id: Route; label: string }[] = [
    { id: 'jobs', label: 'Jobs' },
    { id: 'resume', label: 'Resume' },
    { id: 'ai-search', label: 'AI Search' },
  ]
</script>

<QueryClientProvider client={queryClient}>
  <nav class="border-b border-gray-200 bg-white">
    <div class="mx-auto flex max-w-7xl gap-1 px-6">
      {#each navItems as item (item.id)}
        <button
          class="border-b-2 px-4 py-3 text-sm font-medium transition-colors {route === item.id
            ? 'border-indigo-600 text-indigo-600'
            : 'border-transparent text-gray-500 hover:text-gray-800'}"
          onclick={() => (route = item.id)}
        >
          {item.label}
        </button>
      {/each}
    </div>
  </nav>

  {#if route === 'jobs'}
    <JobsPage />
  {:else if route === 'resume'}
    <ResumePage />
  {:else if route === 'ai-search'}
    <AiSearchPage />
  {/if}
</QueryClientProvider>
