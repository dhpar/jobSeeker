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
- `src/lib/api/` - typed fetch client (`client.ts`), endpoint wrappers (`queries.ts`), types
- `src/lib/stores/filters.svelte.ts` - Svelte 5 runes store for filter state
- `src/lib/search.ts` - pure client-side JD filtering functions (unit-testable, no Svelte deps)
- `src/lib/components/` - page and UI components

## Key conventions

- TanStack Svelte Query v6 results are plain reactive objects: use `query.data`, NOT `$query.data` (no `$` store prefix).
- Queries/mutations must be created during component init (`createQuery(() => ...)`, `useScrapeMutation()`).
- API calls use relative paths (`/jobs`, `/scrape`); the Vite dev proxy forwards them to `http://localhost:8888`. Override with `VITE_API_BASE_URL` for production.
- Styling: Tailwind CSS v4 via `@tailwindcss/vite` plugin (no tailwind.config.js; theme is CSS-first via `@import 'tailwindcss'` in `src/app.css`).

## Extending

- New backend endpoints: add types in `src/lib/api/types.ts`, a wrapper in `queries.ts`, then consume with `createQuery`.
- New features: add a tab/route in `src/App.svelte`. `ResumePage.svelte` and `AiSearchPage.svelte` are intentional stubs for resume customization and AI search.
