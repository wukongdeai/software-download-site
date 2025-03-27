<template>
  <div class="home">
    <el-row :gutter="20">
      <!-- 左侧分类导航 -->
      <el-col :span="4">
        <el-card class="category-card">
          <template #header>
            <div class="card-header">
              <span>软件分类</span>
            </div>
          </template>
          <el-menu
            :default-active="activeCategory"
            class="category-menu"
            @select="handleCategorySelect"
          >
            <el-menu-item
              v-for="category in categories"
              :key="category.id"
              :index="category.id"
            >
              {{ category.name }}
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 右侧软件列表 -->
      <el-col :span="20">
        <el-row :gutter="20">
          <el-col
            v-for="software in softwareList"
            :key="software.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card
              class="software-card"
              :body-style="{ padding: '0px' }"
              @click="goToDetail(software.id)"
            >
              <img :src="software.icon_url" class="software-icon">
              <div class="software-info">
                <h3>{{ software.name }}</h3>
                <p class="description">{{ software.description }}</p>
                <div class="meta-info">
                  <span>
                    <el-icon><Download /></el-icon>
                    {{ software.download_count }}
                  </span>
                  <span>
                    <el-icon><Calendar /></el-icon>
                    {{ formatDate(software.versions[0].release_date) }}
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[12, 24, 36, 48]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Download, Calendar } from '@element-plus/icons-vue'
import { formatDate } from '../utils/date'

const router = useRouter()
const activeCategory = ref('all')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const softwareList = ref([])
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'system', name: '系统工具' },
  { id: 'design', name: '设计软件' },
  { id: 'game', name: '游戏' },
  { id: 'office', name: '办公软件' },
  { id: 'development', name: '开发工具' }
])

const fetchSoftwareList = async () => {
  try {
    const response = await fetch(`/api/software?category=${activeCategory.value}&skip=${(currentPage.value - 1) * pageSize.value}&limit=${pageSize.value}`)
    const data = await response.json()
    softwareList.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('获取软件列表失败:', error)
  }
}

const handleCategorySelect = (categoryId) => {
  activeCategory.value = categoryId
  currentPage.value = 1
  fetchSoftwareList()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchSoftwareList()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchSoftwareList()
}

const goToDetail = (id) => {
  router.push(`/software/${id}`)
}

onMounted(() => {
  fetchSoftwareList()
})
</script>

<style lang="scss" scoped>
.home {
  .category-card {
    margin-bottom: 20px;
  }

  .category-menu {
    border-right: none;
  }

  .software-card {
    margin-bottom: 20px;
    cursor: pointer;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .software-icon {
      width: 100%;
      height: 160px;
      object-fit: cover;
    }

    .software-info {
      padding: 14px;

      h3 {
        margin: 0 0 10px;
        font-size: 16px;
      }

      .description {
        color: #666;
        font-size: 14px;
        margin: 0 0 10px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }

      .meta-info {
        display: flex;
        justify-content: space-between;
        color: #999;
        font-size: 12px;

        span {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
    }
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
}
</style> 