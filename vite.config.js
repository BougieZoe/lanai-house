import { defineConfig } from 'vite';

// GitHub Pages serves project sites from /<repo>/. Local dev and preview keep '/'.
const base = process.env.GITHUB_PAGES ? '/lanai-house/' : '/';

export default defineConfig({
  base,
  build: {
    target: 'es2020',
    cssCodeSplit: true,
    rollupOptions: {
      input: {
        main: 'index.html',
        film: 'film/index.html',
      },
    },
  },
});
