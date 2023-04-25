// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig, loadEnv} from 'vite'
import { fileURLToPath, URL } from 'node:url'

export default({ mode }) => {
    process.env = {...process.env, ...loadEnv(mode, process.cwd())};

    return defineConfig({
      plugins: [
        vue({ 
          template: { transformAssetUrls }
        }),
        // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
        vuetify({
          autoImport: true,
        }),
      ],
      define: { 'process.env': { AUTH_SERVICE: import.meta}},
      resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url)),
          '/auth': process.env.AUTH_SERVICE,
          '/data': process.env.DATA_SERVICE,      
        },
        extensions: [
          '.js',
          '.json',
          '.jsx',
          '.mjs',
          '.ts',
          '.tsx',
          '.vue',
        ],
      },
      server: {
        port: 3000,
      },
    })
}

// // https://vitejs.dev/config/
// export default 
