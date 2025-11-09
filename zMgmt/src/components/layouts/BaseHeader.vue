<script lang="ts" setup>
import { useDark, useToggle } from '@vueuse/core'

// 黑暗模式检测和控制
const isDark = useDark({})
const toggleDark = useToggle(isDark)
</script>

<template>
  <div class="w-full h-full flex items-center">
    <el-row :gutter="20" class="w-full h-full flex items-center">
      <el-col :span="6" class="flex justify-start items-center h-12">
        <span class="text-lg font-bold">Logo</span>
      </el-col>
      <el-col :span="6"><span class="text-lg font-bold">Logo2</span></el-col>
      <el-col :span="6"><span class="text-lg font-bold">Logo3</span></el-col>
      <el-col :span="6" class="flex justify-end items-center h-12">
        <el-button @click="toggleDark()" class="flex items-center">
          {{ isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>