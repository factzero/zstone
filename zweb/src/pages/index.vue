<template>
  <div class="bg-white m-3">
    <div class="p-3">
      <div class="px-3 py-3">
        <el-row
          :gutter="24"
          class="w-full flex items-center justify-center"
          style="margin-left: 0; margin-right: 0"
        >
          <el-col :span="6">
            <el-card shadow="never" class="card-hover">
              <div class="text-center">fasdfa</div>
              <div class="text-center">asfdasdf</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="never" class="card-hover">
              <div class="text-center">fasdfa</div>
              <div class="text-center">asfdasdf</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="never" class="card-hover">
              <div class="text-center">fasdfa</div>
              <div class="text-center">asfdasdf</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="never" class="card-hover">
              <el-button class="!ml-0" :plain="true" @click="open"> Show message </el-button>
              <div class="text-center">fasdfa</div>
              <div class="text-center">asfdasdf</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'

const open = () => {
  ElMessage('This is a message.')
}
</script>

<style scoped>
.card-hover {
  transition: all 0.3s ease;
  cursor: pointer;
}

.card-hover:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  z-index: 10;
}
</style>
