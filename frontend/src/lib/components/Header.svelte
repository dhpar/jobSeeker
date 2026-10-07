<script lang="ts">
  import { useScrapeMutation } from '../api/queries'
  import { scrapeState } from '../stores/scrape.svelte'
  
  const scrapeMutation = useScrapeMutation()
</script>

<header class="border-b border-gray-200 pb-4 mb-4">
    <div class="flex items-center justify-between mx-auto max-w-7xl">
        <h1 class="text-xl font-bold text-gray-900">JobSeeker</h1>
        <p class="text-sm text-gray-500">
            Scraped job listings and JD matching
        </p>
    
        <div class="flex items-center gap-3">
            {#if scrapeState.running}
            <span class="text-sm text-gray-500">Scraping in progress&hellip;</span>
            {:else if scrapeState.error}
            <span class="text-sm text-red-600">{scrapeState.error}</span>
            {/if}
            {#if !scrapeState.connected}
            <span class="text-xs text-amber-600" title="WebSocket disconnected; auto-refresh off">
                live updates off
            </span>
            {/if}
            <button
            class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
            onclick={() => scrapeMutation.mutate()}
            disabled={scrapeState.running || scrapeMutation.isPending}
            >
            {scrapeState.running || scrapeMutation.isPending ? 'Scraping...' : 'Run Scrape'}
            </button>
        </div>
    </div>
</header>