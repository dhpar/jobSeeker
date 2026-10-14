<script lang="ts">
  import { useJobsQuery, useScrapeMutation } from '../api/queries'
  import FilterPanel from './FilterPanel.svelte'
  import JobList from './JobList.svelte'
  import { getFilters } from '../stores/filters.svelte'
  import { filterJobs } from '../search'
    import Header from './Header.svelte';

  const { data, isPending, isError, error} = useJobsQuery();

  const filters = getFilters();

  const filteredJobs = $derived(
    data ? filterJobs(data ?? [], filters) : [],
  );
  
  console.log($inspect(data));
</script>

<Header />

<div class="flex min-h-screen flex-col px-6 py-4 gap-6 bg-slate">
  <main class="flex flex-1 gap-6 mx-auto w-full">
    <aside class="w-1/4 shrink-0">
      <FilterPanel />
    </aside>

    <section class="w-3/4 flex-1">
      {#if isPending}
        <div class="rounded-lg border border-slate bg-turquoise-green p-8 text-center text-gray-500">
          Loading jobs...
        </div>
      {:else if isError}
        <div class="rounded-lg border border-red-200 bg-red-50 p-8 text-center text-red-700">
          Failed to load jobs: {error.message}
        </div>
      {:else if filteredJobs.length === 0 || filterJobs === null}
        <div class="rounded-lg border border-slate bg-turquoise-green p-8 text-center text-gray-500">
          {(data ?? []).length === 0
            ? 'No jobs scraped yet. Click "Run Scrape" to fetch listings.'
            : 'No jobs match the current filters.'}
        </div>
      {:else}
        <div class="mb-3 text-sm text-gray-500">
          {filteredJobs.length} of {data?.length ?? 0} jobs
        </div>
        <JobList jobs={filteredJobs} />
      {/if}
    </section>
  </main>
</div>
