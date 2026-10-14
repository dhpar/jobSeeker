<script module lang="ts">
    export type TRoute = 'jobs' | 'resume' | 'ai-search';
    export const route = $state<{page: TRoute}>({ page: 'jobs' });
</script>

<script lang="ts">
    import { useScrapeMutation } from '../api/queries';
    import { scrapeState } from '../stores/scrape.svelte';
    import { navItems } from '../../App.svelte';

    const scrapeMutation = useScrapeMutation();
    const handleChangeRoute = (itemId:TRoute) => (route.page = itemId);
</script>

<header class="bg-cobalt-green">
    <div class="flex flex-1 w-full justify-between border-b border-turquoise-green bg-slate align-middle px-6">
        <h1 class="text-xl font-bold text-turquoise-green content-center">JobSeeker</h1>
        <nav class="flex gap-1">
            {#each navItems as item (item.id)}
                <button
                    class="border-b-4 px-4 py-3 text-sm font-medium transition-colors {route.page === item.id
                    ? 'border-cobalt-green text-cobalt-green'
                    : 'border-transparent text-turquoise-green hover:text-cobalt-green'}"
                    onclick={() => handleChangeRoute(item.id)}
                >
                  {item.label}
                </button>
            {/each}
        </nav>
    </div>
    <div class="flex items-center justify-between mx-auto px-6 border-b border-turquoise-green py-4">
        <div class="flex items-center gap-3 w-full justify-end">
            Scraped job listings and JD matching
            {#if scrapeState.running}
            <span class="text-sm text-slate">Scraping in progress&hellip;</span>
            {:else if scrapeState.error}
            <span class="text-sm text-red-600">{scrapeState.error}</span>
            {/if}
            <p class="">
                {#if !scrapeState.connected}
                    <span class="text-xs text-amber-600" title="WebSocket disconnected; auto-refresh off">live updates off</span>
                {/if}
                <button
                    class="rounded-md bg-slate px-4 py-2 text-sm font-medium text-turquoise-green border border-solid hover:bg-slate/25 hover:text-slate/90 hover:border-slate/90 disabled:opacity-50"
                    onclick={() => scrapeMutation.mutate()}
                    disabled={scrapeState.running || scrapeMutation.isPending}
                >
                    {scrapeState.running || scrapeMutation.isPending ? 'Scraping...' : 'Run Scrape'}
                </button>
            </p>
        </div>
    </div>
</header>