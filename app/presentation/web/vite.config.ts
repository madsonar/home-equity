import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// SPA servida pelo FastAPI em /ui/* → base precisa ser /ui/
export default defineConfig({
  plugins: [react()],
  base: '/ui/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    chunkSizeWarningLimit: 900,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
