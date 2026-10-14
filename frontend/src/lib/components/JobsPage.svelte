<script lang="ts">
  import { useJobsQuery, useScrapeMutation } from '../api/queries'
  import FilterPanel from './FilterPanel.svelte'
  import JobList from './JobList.svelte'
  import { getFilters } from '../stores/filters.svelte'
  import { filterJobs } from '../search'
    import Header from './Header.svelte';

  const { data, isPending, isError, error, isFetching} = useJobsQuery();

  const filters = getFilters();

  const filteredJobs = $derived(
    data ? filterJobs(data ?? [], filters) : [],
  );
  
  console.log($inspect(data));
</script>

<Header />

<div class="flex min-h-screen flex-col px-6 py-4 gap-6 bg-slate">
  <main class="mx-auto w-full">
      {#if isPending}
        <div class="w-full rounded-lg border border-slate bg-turquoise-green p-8 text-center text-gray-500">
          Press the button to start to scrape
        </div>
      {:else if !data && isFetching}
        <div class="w-full rounded-lg border border-slate bg-turquoise-green p-8 text-center text-gray-500">
          Loading jobs...
        </div>
      {:else if isError}
        <div class="w-full rounded-lg border border-red-200 bg-red-50 p-8 text-center text-red-700">
          Failed to load jobs: {error.message}
        </div>
      {:else if filteredJobs.length === 0 || filterJobs === null}
        <div class="w-full rounded-lg border border-slate bg-turquoise-green p-8 text-center text-gray-500">
          {(data ?? []).length === 0
            ? 'No jobs scraped yet. Click "Run Scrape" to fetch listings.'
            : 'No jobs match the current filters.'}
        </div>
      {:else}
        <div class="grid grid-cols-4 gap-4 w-full">
          <div class="w-full col-span-4 font-bold text-lg text-turquoise-green text-end">
            {filteredJobs.length} of {data?.length ?? 0} jobs
          </div>
          <aside class="col-span-1">
            <FilterPanel />
          </aside>
          <section class="col-span-3">
            <JobList jobs={filteredJobs} />
          </section>
        </div>
      {/if}
  </main>
</div>
