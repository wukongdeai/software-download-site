<template>
  <el-container class="app-container">
    <el-header>
      <nav-bar />
    </el-header>
    <el-main>
      <router-view />
    </el-main>
    <el-footer>
      <footer-bar />
    </el-footer>
  </el-container>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
}

.el-header {
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.el-footer {
  padding: 20px;
  background-color: #f5f7fa;
  text-align: center;
}
</style> 