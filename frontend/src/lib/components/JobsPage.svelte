<script lang="ts">
  import { useJobsQuery, useScrapeMutation } from '../api/queries'
  import FilterPanel from './FilterPanel.svelte'
  import JobList from './JobList.svelte'
  import { getFilters } from '../stores/filters.svelte'
  import { filterJobs } from '../search'

  const jobsQuery = useJobsQuery()
  const scrapeMutation = useScrapeMutation()
  const filters = getFilters()

  const filteredJobs = $derived(
    jobsQuery.data ? filterJobs(jobsQuery.data.data ?? [], filters) : [],
  )
</script>

<div class="flex min-h-screen flex-col bg-gray-50">
  <header class="border-b border-gray-200 bg-white px-6 py-4">
    <div class="mx-auto flex max-w-7xl items-center justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">JobSeeker</h1>
        <p class="text-sm text-gray-500">Scraped job listings and JD matching</p>
      </div>
      <div class="flex items-center gap-3">
        {#if scrapeMutation.isPending}
          <span class="text-sm text-gray-500">Scraping...</span>
        {:else if scrapeMutation.isSuccess}
          <span class="text-sm text-gray-500">{scrapeMutation.data.status}</span>
        {:else if scrapeMutation.isError}
          <span class="text-sm text-red-600">Scrape failed</span>
        {/if}
        <button
          class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
          onclick={() => scrapeMutation.mutate()}
          disabled={scrapeMutation.isPending}
        >
          {scrapeMutation.isPending ? 'Scraping...' : 'Run Scrape'}
        </button>
      </div>
    </div>
  </header>

  <main class="mx-auto flex w-full max-w-7xl flex-1 gap-6 px-6 py-6">
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
