import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import VueRouter from 'unplugin-vue-router/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    VueRouter({}),
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      //导入自己的组件 指定组件位置，默认是src/components
      dirs: ['src/views'],
      // ui解析库
      resolvers: [ElementPlusResolver()],
      //配置文件生成位置, 插件会生成一个自己组件路径的components.d.ts文件
      dts: './.components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
