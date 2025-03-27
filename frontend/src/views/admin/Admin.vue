<template>
  <div class="admin-container">
    <el-row :gutter="20">
      <!-- 左侧菜单 -->
      <el-col :span="4">
        <el-card class="menu-card">
          <el-menu
            :default-active="activeMenu"
            class="admin-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="software">
              <el-icon><Monitor /></el-icon>
              <span>软件管理</span>
            </el-menu-item>
            <el-menu-item index="users">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="categories">
              <el-icon><Folder /></el-icon>
              <span>分类管理</span>
            </el-menu-item>
            <el-menu-item index="stats">
              <el-icon><DataLine /></el-icon>
              <span>统计面板</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 右侧内容 -->
      <el-col :span="20">
        <el-card>
          <!-- 软件管理 -->
          <template v-if="activeMenu === 'software'">
            <template #header>
              <div class="card-header">
                <span>软件管理</span>
                <el-button type="primary" @click="showAddSoftwareDialog">
                  添加软件
                </el-button>
              </div>
            </template>
            
            <el-table :data="softwareList" style="width: 100%">
              <el-table-column prop="name" label="软件名称" />
              <el-table-column prop="category" label="分类" />
              <el-table-column prop="download_count" label="下载量" />
              <el-table-column prop="versions[0].version_number" label="最新版本" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button-group>
                    <el-button size="small" @click="handleEdit(scope.row)">
                      编辑
                    </el-button>
                    <el-button
                      size="small"
                      type="danger"
                      @click="handleDelete(scope.row)"
                    >
                      删除
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </template>

          <!-- 用户管理 -->
          <template v-if="activeMenu === 'users'">
            <template #header>
              <div class="card-header">
                <span>用户管理</span>
              </div>
            </template>
            
            <el-table :data="userList" style="width: 100%">
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="email" label="邮箱" />
              <el-table-column prop="is_admin" label="管理员">
                <template #default="scope">
                  <el-tag :type="scope.row.is_admin ? 'danger' : 'info'">
                    {{ scope.row.is_admin ? '是' : '否' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button-group>
                    <el-button
                      size="small"
                      :type="scope.row.is_admin ? 'warning' : 'success'"
                      @click="handleToggleAdmin(scope.row)"
                    >
                      {{ scope.row.is_admin ? '取消管理员' : '设为管理员' }}
                    </el-button>
                    <el-button
                      size="small"
                      type="danger"
                      @click="handleDeleteUser(scope.row)"
                    >
                      删除
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </template>

          <!-- 分类管理 -->
          <template v-if="activeMenu === 'categories'">
            <template #header>
              <div class="card-header">
                <span>分类管理</span>
                <el-button type="primary" @click="showAddCategoryDialog">
                  添加分类
                </el-button>
              </div>
            </template>
            
            <el-table :data="categoryList" style="width: 100%">
              <el-table-column prop="name" label="分类名称" />
              <el-table-column prop="description" label="描述" />
              <el-table-column label="操作" width="200">
                <template #default="scope">
                  <el-button-group>
                    <el-button size="small" @click="handleEditCategory(scope.row)">
                      编辑
                    </el-button>
                    <el-button
                      size="small"
                      type="danger"
                      @click="handleDeleteCategory(scope.row)"
                    >
                      删除
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
          </template>

          <!-- 统计面板 -->
          <template v-if="activeMenu === 'stats'">
            <template #header>
              <div class="card-header">
                <span>统计面板</span>
              </div>
            </template>
            
            <el-row :gutter="20">
              <el-col :span="6">
                <el-card shadow="hover">
                  <template #header>
                    <div class="stat-header">
                      <span>总软件数</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ stats.totalSoftware }}</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <template #header>
                    <div class="stat-header">
                      <span>总用户数</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ stats.totalUsers }}</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <template #header>
                    <div class="stat-header">
                      <span>今日下载量</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ stats.todayDownloads }}</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card shadow="hover">
                  <template #header>
                    <div class="stat-header">
                      <span>总下载量</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ stats.totalDownloads }}</div>
                </el-card>
              </el-col>
            </el-row>

            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span>下载趋势</span>
                </div>
              </template>
              <!-- 这里可以集成图表库，如 ECharts -->
            </el-card>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加/编辑软件对话框 -->
    <el-dialog
      v-model="softwareDialogVisible"
      :title="editingSoftware ? '编辑软件' : '添加软件'"
      width="50%"
    >
      <el-form
        ref="softwareFormRef"
        :model="softwareForm"
        :rules="softwareRules"
        label-width="100px"
      >
        <el-form-item label="软件名称" prop="name">
          <el-input v-model="softwareForm.name" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="softwareForm.category">
            <el-option
              v-for="category in categoryList"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="softwareForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="图标" prop="icon_url">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleIconSuccess"
          >
            <img v-if="softwareForm.icon_url" :src="softwareForm.icon_url" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="softwareDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveSoftware">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  Monitor,
  User,
  Folder,
  DataLine,
  Plus
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeMenu = ref('software')
const softwareDialogVisible = ref(false)
const editingSoftware = ref(null)
const softwareFormRef = ref(null)

// 数据列表
const softwareList = ref([])
const userList = ref([])
const categoryList = ref([])
const stats = ref({
  totalSoftware: 0,
  totalUsers: 0,
  todayDownloads: 0,
  totalDownloads: 0
})

// 表单数据
const softwareForm = reactive({
  name: '',
  category: '',
  description: '',
  icon_url: ''
})

// 表单验证规则
const softwareRules = {
  name: [
    { required: true, message: '请输入软件名称', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' }
  ]
}

// 菜单选择
const handleMenuSelect = (index) => {
  activeMenu.value = index
  fetchData()
}

// 获取数据
const fetchData = async () => {
  try {
    switch (activeMenu.value) {
      case 'software':
        const softwareResponse = await fetch('/api/admin/software')
        softwareList.value = await softwareResponse.json()
        break
      case 'users':
        const userResponse = await fetch('/api/admin/users')
        userList.value = await userResponse.json()
        break
      case 'categories':
        const categoryResponse = await fetch('/api/admin/categories')
        categoryList.value = await categoryResponse.json()
        break
      case 'stats':
        const statsResponse = await fetch('/api/admin/stats')
        stats.value = await statsResponse.json()
        break
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

// 软件相关操作
const showAddSoftwareDialog = () => {
  editingSoftware.value = null
  Object.assign(softwareForm, {
    name: '',
    category: '',
    description: '',
    icon_url: ''
  })
  softwareDialogVisible.value = true
}

const handleEdit = (software) => {
  editingSoftware.value = software
  Object.assign(softwareForm, software)
  softwareDialogVisible.value = true
}

const handleDelete = async (software) => {
  try {
    await ElMessageBox.confirm('确定要删除该软件吗？', '提示', {
      type: 'warning'
    })
    await fetch(`/api/admin/software/${software.id}`, {
      method: 'DELETE'
    })
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleSaveSoftware = async () => {
  if (!softwareFormRef.value) return
  
  try {
    await softwareFormRef.value.validate()
    const url = editingSoftware.value
      ? `/api/admin/software/${editingSoftware.value.id}`
      : '/api/admin/software'
    const method = editingSoftware.value ? 'PUT' : 'POST'
    
    await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(softwareForm)
    })
    
    ElMessage.success(editingSoftware.value ? '更新成功' : '添加成功')
    softwareDialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  }
}

const handleIconSuccess = (response) => {
  softwareForm.icon_url = response.url
}

// 用户相关操作
const handleToggleAdmin = async (user) => {
  try {
    await fetch(`/api/admin/users/${user.id}/toggle-admin`, {
      method: 'POST'
    })
    ElMessage.success('操作成功')
    fetchData()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleDeleteUser = async (user) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      type: 'warning'
    })
    await fetch(`/api/admin/users/${user.id}`, {
      method: 'DELETE'
    })
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 分类相关操作
const showAddCategoryDialog = () => {
  // 实现添加分类的逻辑
}

const handleEditCategory = (category) => {
  // 实现编辑分类的逻辑
}

const handleDeleteCategory = async (category) => {
  try {
    await ElMessageBox.confirm('确定要删除该分类吗？', '提示', {
      type: 'warning'
    })
    await fetch(`/api/admin/categories/${category.id}`, {
      method: 'DELETE'
    })
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.admin-container {
  .menu-card {
    margin-bottom: 20px;
  }

  .admin-menu {
    border-right: none;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #409EFF;
    text-align: center;
  }

  .chart-card {
    margin-top: 20px;
  }

  .avatar-uploader {
    :deep(.el-upload) {
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);

      &:hover {
        border-color: var(--el-color-primary);
      }
    }
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
  }

  .avatar {
    width: 100px;
    height: 100px;
    display: block;
  }
}
</style> 