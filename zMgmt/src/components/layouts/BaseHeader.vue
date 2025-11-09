<script lang="ts" setup>
import { ref } from "vue";
import { useDark, useToggle } from "@vueuse/core";
import { Sunny, Moon } from "@element-plus/icons-vue";

const isDark = useDark();
const toggleDark = useToggle(isDark);

const pos = ref({ x: 0, y: 0 });

function onClick(e: MouseEvent) {
  pos.value = { x: e.clientX, y: e.clientY };
}

function onChange(val: boolean) {
  const setTheme = () => {
    toggleDark(val);
  };

  const doAnimate = () => {
    const radius = Math.hypot(
      Math.max(pos.value.x, window.innerWidth - pos.value.x),
      Math.max(pos.value.y, window.innerHeight - pos.value.y),
    );

    const clipPath = [
      `circle(0px at ${pos.value.x}px ${pos.value.y}px)`,
      `circle(${radius}px at ${pos.value.x}px ${pos.value.y}px)`,
    ];

    document.documentElement.animate(
      { clipPath: val ? clipPath.reverse() : clipPath },
      {
        duration: 600,
        pseudoElement: val
          ? "::view-transition-old(root)"
          : "::view-transition-new(root)",
      },
    );
  };

  document.startViewTransition
    ? document.startViewTransition(setTheme).ready.then(doAnimate)
    : setTheme();
}
</script>

<template>
  <div class="w-full h-full">
    <el-row :gutter="20" class="w-full h-full flex items-center">
      <el-col :span="6" class="flex justify-start items-center">
        <span class="text-lg font-bold">Logo</span>
      </el-col>
      <el-col :span="18">
        <div class="flex justify-end items-center">
          <el-switch
            class="XSwitchTheme"
            :model-value="isDark"
            @change="onChange"
            @click.capture="onClick"
            style="
              --el-switch-on-color: #606266;
              --el-switch-off-color: #e6e8eb;
            "
          >
            <template #inactive-action>
              <el-icon style="color: #000000"><Sunny /></el-icon>
            </template>
            <template #active-action>
              <el-icon style="color: #000000"><Moon /></el-icon>
            </template>
          </el-switch>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style>
.XSwitchTheme {
  .el-switch__action {
    background-color: transparent;
  }
}

::view-transition-new(root),
::view-transition-old(root) {
  animation: none;
  mix-blend-mode: normal;
}
.dark::view-transition-old(root) {
  z-index: 9999;
}
</style>
