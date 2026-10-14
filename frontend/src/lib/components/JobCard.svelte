<script lang="ts">
  import type { Job } from '../api/types'

  interface Props {
    job: Job
  }

  let { job }: Props = $props()
  let expanded = $state(false)
  $inspect(job);
  const snippet = $derived(job.text.length > 240 && !expanded ? job.text.slice(0, 240) + '...' : job.text)
</script>

<article class="rounded-lg border border-gray-200 bg-turquoise-green p-4 shadow-sm">
  <div class="flex items-start justify-between gap-4">
    <div class="min-w-0">
      <h3 class="truncate text-base font-semibold text-gray-900">{job.title}</h3>
      <p class="mt-0.5 text-sm text-gray-600">{job.company}</p>
      <div class="mt-2 flex flex-wrap items-center gap-2 text-xs">
        <span class="rounded bg-gray-100 px-2 py-0.5 font-medium text-gray-600">{job.source}</span>
        {#if job.location}
          <span class="text-gray-500">{job.location}</span>
        {/if}
      </div>
    </div>
    <a
      href={job.url}
      target="_blank"
      rel="noopener noreferrer"
      class="rounded-md bg-slate px-4 py-2 text-sm font-medium text-turquoise-green border border-solid hover:bg-slate/25 hover:text-slate/90 hover:border-slate/90 disabled:opacity-50"
    >
      Open
    </a>
  </div>

  <p class="mt-3 whitespace-pre-line text-sm leading-relaxed text-gray-700">{snippet}</p>

  {#if job.text.length > 240}
    <button
      class="mt-2 text-md font-medium text-slate/90 hover:underline"
      onclick={() => (expanded = !expanded)}
    >
      {expanded ? 'Show less' : 'Show more'}
    </button>
  {/if}
</article>
