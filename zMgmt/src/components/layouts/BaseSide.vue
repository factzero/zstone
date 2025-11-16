<script lang="ts" setup>
import { useRouter } from "vue-router";
import { Document } from "@element-plus/icons-vue";

const router = useRouter();

// 菜单点击处理
const handleMenuClick = (path: string) => {
  router.push(path);
};
</script>

<template>
  <div class="h-full bg-gray-800 text-white w-64">
    <div class="flex items-center justify-center h-16 border-b border-gray-700">
      <h1 class="text-xl font-bold">考试系统</h1>
    </div>

    <el-menu
      class="border-none bg-gray-800 text-white"
      :default-active="$route.path"
      @select="handleMenuClick"
    >
      <el-menu-item index="/qmgr">
        <el-icon><Document /></el-icon>
        <span>试题管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<style scoped>
.el-menu {
  border-right: none !important;
}

:deep(.el-menu-item:hover) {
  background-color: #4b5563 !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #3b82f6 !important;
  color: white !important;
}
</style>