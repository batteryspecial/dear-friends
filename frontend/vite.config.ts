import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import path from 'path'
import fs from 'fs'

// After build, move index.html from static/ into Django's templates directory
const moveHtmlToDjangoTemplates = () => ({
  name: 'move-html-to-django-templates',
  closeBundle() {
    const src = path.resolve(__dirname, '../backend/static/frontend/index.html')
    const dest = path.resolve(__dirname, '../backend/web/templates/web/index.html')
    fs.mkdirSync(path.dirname(dest), { recursive: true })
    fs.copyFileSync(src, dest)
    fs.unlinkSync(src)
  },
})

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    vueDevTools(),
    moveHtmlToDjangoTemplates(),
  ],
  // In production, asset URLs must match Django's STATIC_URL + the output folder
  base: process.env.NODE_ENV === 'production' ? '/static/frontend/' : '/',
  build: {
    outDir: path.resolve(__dirname, '../backend/static/frontend'),
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
