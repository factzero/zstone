<template>
  <div class="w-full h-full bg-gray-600">
    <BaseHeader class="header w-full fixed top-0 z-10" />
    <div class="content w-full p-1">
      <router-view />
    </div>
    <BaseFooter class="bg-sky-950 text-white" />
  </div>
</template>

<script setup lang="ts">
// 无需额外的 script 代码
</script>

<style scoped>
.header {
  height: 64px;
}

.content {
  position: relative;
  margin-top: 64px; /* 与 header 高度一致 */
}
</style>
