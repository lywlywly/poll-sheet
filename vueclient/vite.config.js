import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  // assetsInclude(file) {
  //   return /\.(txt)$/.test(file)
  // },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.md/,
          type: 'asset/source',
        }
      ]
    },
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
