/// <reference types="vitest/config" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
    globals: true, // Rend les API de Vitest (describe, test, expect) globales
    exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
  },
})
