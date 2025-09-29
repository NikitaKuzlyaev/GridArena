import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  root: '.', // корень — папка с index.html и package.json (frontend)
  base: '/', // фикс бага на проде
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/react/src' // алиас для удобства импорта из react/src
    }
  },
  build: {
    outDir: 'dist', // куда билдить, относительно root
    emptyOutDir: true,
  }
})
