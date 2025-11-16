<template>
  <div class="w-full h-full bg-white">
    <el-row :gutter="24" class="w-full h-full flex justify-center items-center">
      <el-col :span="4" :offset="1">
        <div class="flex justify-center items-center h-full">
          <img src="@/assets/images/logo.png" alt="Logo" class="h-16 w-auto object-contain" />
        </div>
      </el-col>
      <el-col :span="14" :offset="1">
        <el-row :gutter="24">
          <el-col :span="4">
            <router-link to="/" class="nav-item" exact-active-class="nav-item-active">
              题库
            </router-link>
          </el-col>
          <el-col :span="4">
            <router-link to="/StatInfo" class="nav-item" active-class="nav-item-active">
              统计
            </router-link>
          </el-col>
          <el-col :span="4">
            <router-link to="/PriceInfo" class="nav-item" active-class="nav-item-active">
              定价
            </router-link>
          </el-col>
          <el-col :span="4">
            <router-link to="/RebBook" class="nav-item" active-class="nav-item-active">
              宝书
            </router-link>
          </el-col>
          <el-col :span="4">
            <router-link to="/ThesisAssistant" class="nav-item" active-class="nav-item-active">
              论文助手
            </router-link>
          </el-col>
          <el-col :span="4">
            <router-link to="/DownloadApp" class="nav-item" active-class="nav-item-active">
              APP
            </router-link>
          </el-col>
        </el-row>
      </el-col>
      <el-col :span="2" :offset="2">
        <div class="nav-item">登录</div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// 无需额外的 script 代码
</script>

<style scoped>
.nav-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-decoration: none;
  color: #909399;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 4px;
  font-size: 18px;
  position: relative;
}

.nav-item:hover {
  color: #409eff;
}

.nav-item-active {
  color: #409eff;
  font-weight: bold;
}

.nav-item-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 50%;
  height: 2px;
  background-color: #409eff;
}
</style>
