<script setup lang="ts"></script>

<template>
  <div class="app-container">
    <el-container class="main-container">
      <el-header class="layout-header"><BaseHeader /></el-header>
      <el-divider style="margin: 0; height: 1px" />
      <el-container class="flex-container">
        <el-aside width="200px" class="layout-aside"><BaseSide /></el-aside>
        <el-divider
          direction="vertical"
          style="margin: 0; height: auto; width: 1px"
        />
        <el-container class="content-container">
          <el-main class="main-content"><RouterView /></el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.app-container {
  height: 100vh; /* 视口高度 */
  width: 100vw; /* 视口宽度 */
  overflow: hidden; /* 防止出现滚动条 */
}

.main-container {
  height: 100%;
}

.flex-container {
  height: calc(
    100% - 60px
  ); /* 减去 header 的高度，具体值根据实际 header 高度调整 */
}

.content-container {
  flex: 1;
  height: 100%;
}

.main-content {
  height: 100%;
  overflow-y: auto; /* 如果内容超出，允许滚动 */
}
</style>
