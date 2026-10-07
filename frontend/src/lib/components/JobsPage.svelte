<script lang="ts">
  import { useJobsQuery, useScrapeMutation } from '../api/queries'
  import FilterPanel from './FilterPanel.svelte'
  import JobList from './JobList.svelte'
  import { getFilters } from '../stores/filters.svelte'
  import { filterJobs } from '../search'
    import Header from './Header.svelte';

  const jobsQuery = useJobsQuery()
  const filters = getFilters()

  const filteredJobs = $derived(
    jobsQuery.data ? filterJobs(jobsQuery.data.data ?? [], filters) : [],
  )
</script>

<div class="flex min-h-screen flex-col px-6 py-4 gap-6 bg-gray-50">
  <Header />

  <main class="flex flex-1 gap-6 mx-auto max-w-7xl">
    <aside class="w-72 shrink-0">
      <FilterPanel />
    </aside>

    <section class="flex-1">
      {#if jobsQuery.isPending}
        <div class="rounded-lg border border-gray-200 bg-white p-8 text-center text-gray-500">
          Loading jobs...
        </div>
      {:else if jobsQuery.isError}
        <div class="rounded-lg border border-red-200 bg-red-50 p-8 text-center text-red-700">
          Failed to load jobs: {jobsQuery.error.message}
        </div>
      {:else if filteredJobs.length === 0}
        <div class="rounded-lg border border-gray-200 bg-white p-8 text-center text-gray-500">
          {(jobsQuery.data?.data ?? []).length === 0
            ? 'No jobs scraped yet. Click "Run Scrape" to fetch listings.'
            : 'No jobs match the current filters.'}
        </div>
      {:else}
        <div class="mb-3 text-sm text-gray-500">
          {filteredJobs.length} of {jobsQuery.data?.data?.length ?? 0} jobs
        </div>
        <JobList jobs={filteredJobs} />
      {/if}
    </section>
  </main>
</div>
