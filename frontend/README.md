# JobSeeker Frontend

Svelte 5 + TypeScript + TanStack Query UI for the JobSeeker backend.

## Commands

```bash
npm install        # install deps
npm run dev        # dev server on http://localhost:5173
npm run check      # svelte-check + tsc (typecheck) - run this before committing
npm run build      # production build to dist/
npm run preview    # preview the production build
```

## Architecture

- `src/main.ts` - mounts `App.svelte` (Svelte 5 `mount`, not `new App()`)
- `src/App.svelte` - QueryClientProvider + tab navigation (Jobs / Resume / AI Search)
- `src/lib/api/` - typed fetch client (`client.ts`, `queries.ts`), WebSocket scrape-progress client (`ws.ts`), types
- `src/lib/stores/` - Svelte 5 runes stores (`filters.svelte.ts`, `scrape.svelte.ts`)
- `src/lib/search.ts` - pure client-side JD filtering functions (unit-testable, no Svelte deps)
- `src/lib/components/` - page and UI components

## Key conventions

- TanStack Svelte Query v6 results are plain reactive objects: use `query.data`, NOT `$query.data` (no `$` store prefix).
- Queries/mutations must be created during component init (`createQuery(() => ...)`, `useScrapeMutation()`).
- API calls use relative paths (`/jobs`, `/scrape`); the Vite dev proxy forwards them to `http://localhost:8888`. Override with `VITE_API_BASE_URL` for production.
- Live updates: `connectScrapeSocket(queryClient)` starts from App.svelte (`onMount`), auto-reconnects with backoff, and on a `/ws` `scrape_completed` event invalidates the jobs query. `scrapeState` (`stores/scrape.svelte.ts`) drives the JobsPage running/error indicator; the Vite proxy forwards `/ws`.
- Styling: Tailwind CSS v4 via `@tailwindcss/vite` plugin (no tailwind.config.js; theme is CSS-first via `@import 'tailwindcss'` in `src/app.css`).

## Extending

- New backend endpoints: add types in `src/lib/api/types.ts`, a wrapper in `queries.ts`, then consume with `createQuery`.
- New features: add a tab/route in `src/App.svelte`. `ResumePage.svelte` and `AiSearchPage.svelte` are intentional stubs for resume customization and AI search.
