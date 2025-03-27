<template>
  <div class="software-detail">
    <el-card v-if="software" class="detail-card">
      <div class="header">
        <div class="software-info">
          <img :src="software.icon_url" class="software-icon">
          <div class="info">
            <h1>{{ software.name }}</h1>
            <p class="description">{{ software.description }}</p>
            <div class="meta">
              <span>
                <el-icon><Download /></el-icon>
                {{ software.download_count }} 次下载
              </span>
              <span>
                <el-icon><Calendar /></el-icon>
                更新于 {{ formatDate(software.versions[0].release_date) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <el-divider />

      <div class="version-info">
        <h2>版本信息</h2>
        <el-table :data="software.versions" style="width: 100%">
          <el-table-column prop="version_number" label="版本号" width="120" />
          <el-table-column prop="release_date" label="发布日期" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.release_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="file_size" label="文件大小" width="120" />
          <el-table-column label="下载链接">
            <template #default="scope">
              <div v-for="link in scope.row.download_links" :key="link.platform" class="download-link">
                <el-button
                  type="primary"
                  @click="handleDownload(link)"
                  :icon="getPlatformIcon(link.platform)"
                >
                  {{ link.platform }}
                </el-button>
                <el-tag v-if="link.password" size="small" type="warning">提取码: {{ link.password }}</el-tag>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <el-divider />

      <div class="security-info">
        <h2>安全信息</h2>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="MD5">
            {{ software.versions[0].md5 || '暂无' }}
          </el-descriptions-item>
          <el-descriptions-item label="SHA1">
            {{ software.versions[0].sha1 || '暂无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <el-divider />

      <div class="changelog">
        <h2>更新日志</h2>
        <el-timeline>
          <el-timeline-item
            v-for="version in software.versions"
            :key="version.version_number"
            :timestamp="formatDate(version.release_date)"
            placement="top"
          >
            <el-card>
              <h4>版本 {{ version.version_number }}</h4>
              <p>{{ version.changelog || '暂无更新说明' }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Download, Calendar } from '@element-plus/icons-vue'
import { formatDate } from '../utils/date'

const route = useRoute()
const software = ref(null)

const fetchSoftwareDetail = async () => {
  try {
    const response = await fetch(`/api/software/${route.params.id}`)
    software.value = await response.json()
  } catch (error) {
    console.error('获取软件详情失败:', error)
  }
}

const handleDownload = (link) => {
  window.open(link.url, '_blank')
}

const getPlatformIcon = (platform) => {
  const icons = {
    '百度网盘': 'Download',
    '阿里云盘': 'Download',
    'Google Drive': 'Download'
  }
  return icons[platform] || 'Download'
}

onMounted(() => {
  fetchSoftwareDetail()
})
</script>

<style lang="scss" scoped>
.software-detail {
  .detail-card {
    .header {
      .software-info {
        display: flex;
        gap: 20px;

        .software-icon {
          width: 120px;
          height: 120px;
          object-fit: cover;
          border-radius: 8px;
        }

        .info {
          flex: 1;

          h1 {
            margin: 0 0 10px;
            font-size: 24px;
          }

          .description {
            color: #666;
            margin: 0 0 15px;
            line-height: 1.6;
          }

          .meta {
            display: flex;
            gap: 20px;
            color: #999;

            span {
              display: flex;
              align-items: center;
              gap: 4px;
            }
          }
        }
      }
    }

    .version-info {
      h2 {
        margin: 0 0 20px;
      }

      .download-link {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
      }
    }

    .security-info {
      h2 {
        margin: 0 0 20px;
      }
    }

    .changelog {
      h2 {
        margin: 0 0 20px;
      }

      .el-timeline {
        padding-left: 20px;
      }
    }
  }
}
</style> 