<script lang="ts">
  import { getFilters, setFilter, toggleSource, resetFilters, parseCsv } from '../stores/filters.svelte'

  const filters = getFilters()
  const knownSources = ['greenhouse', 'lever', 'ashby', 'hn']

  let keywordInput = $state('')
  let anyKeywordInput = $state('')

  $effect(() => {
    setFilter('keywords', parseCsv(keywordInput))
  })

  $effect(() => {
    setFilter('anyKeywords', parseCsv(anyKeywordInput))
  })
</script>

<div class="space-y-5 rounded-lg border border-gray-200 bg-white p-4">
  <div>
    <label class="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500" for="q">
      Search
    </label>
    <input
      id="q"
      type="search"
      placeholder="Title, company, location, JD..."
      class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
      value={filters.query}
      oninput={(e) => setFilter('query', e.currentTarget.value)}
    />
  </div>

  <div>
    <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500">Source</span>
    <div class="flex flex-wrap gap-2">
      {#each knownSources as source (source)}
        <button
          class="rounded-full border px-3 py-1 text-xs transition-colors {filters.sources.includes(source)
            ? 'border-indigo-600 bg-indigo-600 text-white'
            : 'border-gray-300 bg-white text-gray-600 hover:bg-gray-100'}"
          onclick={() => toggleSource(source)}
        >
          {source}
        </button>
      {/each}
    </div>
  </div>

  <div class="flex items-center gap-2">
    <input
      id="remote"
      type="checkbox"
      class="h-4 w-4 rounded border-gray-300 text-indigo-600"
      checked={filters.remoteOnly}
      onchange={(e) => setFilter('remoteOnly', e.currentTarget.checked)}
    />
    <label for="remote" class="text-sm text-gray-700">Remote only</label>
  </div>

  <div>
    <label class="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500" for="kw">
      Must contain (comma-separated)
    </label>
    <input
      id="kw"
      type="text"
      placeholder="react, typescript"
      class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
      bind:value={keywordInput}
    />
  </div>

  <div>
    <label class="mb-1 block text-xs font-semibold uppercase tracking-wide text-gray-500" for="anykw">
      Any of (comma-separated)
    </label>
    <input
      id="anykw"
      type="text"
      placeholder="remote, hybrid"
      class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
      bind:value={anyKeywordInput}
    />
  </div>

  <button
    class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-600 hover:bg-gray-50"
    onclick={resetFilters}
  >
    Reset filters
  </button>
</div>
