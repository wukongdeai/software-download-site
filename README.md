# 软件下载网站

一个基于Vue 3 + FastAPI的软件下载网站，支持软件管理、用户管理、下载统计等功能。

## 技术栈

### 前端
- Vue 3
- Element Plus
- Vue Router
- Pinia
- Axios

### 后端
- Python FastAPI
- MongoDB
- JWT认证
- Motor (异步MongoDB驱动)

### 部署
- Docker
- Docker Compose
- Nginx

## 功能特点

- 瀑布流/卡片式布局展示软件列表
- 支持分类筛选和搜索
- 软件详情页展示版本信息和下载链接
- 多网盘链接支持
- 安全检测标识（MD5/SHA1校验码）
- 后台管理系统
- 下载量统计
- 链接失效监测

## 快速开始

### 环境要求

- Docker
- Docker Compose
- Node.js 16+ (开发环境)
- Python 3.9+ (开发环境)
- MongoDB (开发环境)

### 使用Docker部署

1. 克隆项目
```bash
git clone <repository-url>
cd software-download-site
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，设置必要的环境变量
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问网站
- 前端: http://localhost
- 后端API: http://localhost:8000
- 管理后台: http://localhost/admin

### 开发环境设置

1. 安装前端依赖
```bash
cd frontend
npm install
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 启动开发服务器
```bash
# 前端
cd frontend
npm run serve

# 后端
cd backend
uvicorn main:app --reload
```

## 项目结构

```
.
├── frontend/                # 前端项目
│   ├── src/                # 源代码
│   ├── public/             # 静态资源
│   └── package.json        # 依赖配置
├── backend/                # 后端项目
│   ├── routers/           # 路由
│   ├── models/            # 数据模型
│   └── main.py            # 主程序
├── nginx/                  # Nginx配置
├── docker-compose.yml      # Docker编排配置
└── README.md              # 项目说明
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档。

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License 