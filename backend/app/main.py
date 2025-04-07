from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, tools, categories, users, comments, favorites, ratings, tutorials, recommendations, statistics, search, compare, usage, category_management, system_config, tag, permission, version, log, subscription, share
from app.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="AI Hub API", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["favorites"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])
app.include_router(tutorials.router, prefix="/api/tutorials", tags=["tutorials"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
app.include_router(statistics.router, prefix="/api", tags=["statistics"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(compare.router, prefix="/api", tags=["compare"])
app.include_router(usage.router, prefix="/api", tags=["usage"])
app.include_router(category_management.router, prefix="/api", tags=["category_management"])
app.include_router(system_config.router, prefix="/api", tags=["system_config"])
app.include_router(tag.router, prefix="/api", tags=["tag"])
app.include_router(permission.router, prefix="/api", tags=["permission"])
app.include_router(version.router, prefix="/api", tags=["version"])
app.include_router(log.router, prefix="/api", tags=["log"])
app.include_router(subscription.router, prefix="/api", tags=["subscription"])
app.include_router(share.router, prefix="/api", tags=["share"])

# 数据库连接事件
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to AI Hub API"} 