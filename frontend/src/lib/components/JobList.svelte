<script lang="ts">
  import type { Job } from '../api/types'
  import JobCard from './JobCard.svelte'

  interface Props {
    jobs: Job[]
  }

  let { jobs }: Props = $props()
</script>

<div class="space-y-4">
  {#each jobs as job (job.url)}
    <JobCard {job} />
  {/each}
</div>
