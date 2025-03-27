<template>
  <div class="nav-container">
    <div class="nav-content">
      <div class="logo">
        <router-link to="/">
          <h1>软件下载站</h1>
        </router-link>
      </div>
      
      <el-menu
        mode="horizontal"
        :router="true"
        class="nav-menu"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/categories">分类</el-menu-item>
        <el-menu-item index="/latest">最新</el-menu-item>
        <el-menu-item index="/popular">热门</el-menu-item>
      </el-menu>

      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索软件..."
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <div class="user-actions">
        <template v-if="isLoggedIn">
          <el-dropdown>
            <span class="user-info">
              {{ username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')">个人中心</el-dropdown-item>
                <el-dropdown-item v-if="isAdmin" @click="$router.push('/admin')">管理后台</el-dropdown-item>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" @click="$router.push('/login')">登录</el-button>
          <el-button @click="$router.push('/register')">注册</el-button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { Search, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const searchQuery = ref('')

const isLoggedIn = computed(() => userStore.isLoggedIn)
const username = computed(() => userStore.username)
const isAdmin = computed(() => userStore.isAdmin)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.nav-container {
  background-color: #fff;
  height: 60px;
  display: flex;
  align-items: center;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  margin-right: 40px;
  
  h1 {
    margin: 0;
    font-size: 24px;
    color: #409EFF;
  }
}

.nav-menu {
  flex: 1;
  border-bottom: none;
}

.search-box {
  width: 300px;
  margin: 0 20px;
}

.user-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  color: #606266;
}
</style> 