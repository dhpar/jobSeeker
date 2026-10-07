import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), svelte()],
  server: {
    proxy: {
      '/jobs': 'http://localhost:8888',
      '/scrape': 'http://localhost:8888',
      '/api': 'http://localhost:8888',
      '/docs': 'http://localhost:8888',
      '/openapi.json': 'http://localhost:8888',
    },
  },
})
