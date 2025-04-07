from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.log import Log, LogQuery
from ..models.user import User
from ..auth import get_current_user, is_admin
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/logs", response_model=Log)
async def create_log(
    log: Log,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """创建日志记录"""
    result = db.logs.insert_one(log.dict(exclude={"id"}))
    log.id = str(result.inserted_id)
    return log

@router.get("/logs", response_model=List[Log])
async def get_logs(
    query: LogQuery = Depends(),
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取日志列表"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    filter_query = {}
    if query.level:
        filter_query["level"] = query.level
    if query.module:
        filter_query["module"] = query.module
    if query.action:
        filter_query["action"] = query.action
    if query.user_id:
        filter_query["user_id"] = query.user_id
    if query.start_time or query.end_time:
        filter_query["created_at"] = {}
        if query.start_time:
            filter_query["created_at"]["$gte"] = query.start_time
        if query.end_time:
            filter_query["created_at"]["$lte"] = query.end_time
    
    logs = list(
        db.logs.find(filter_query)
        .sort("created_at", -1)
        .skip(query.skip)
        .limit(query.limit)
    )
    
    return logs

@router.get("/logs/{log_id}", response_model=Log)
async def get_log(
    log_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取单个日志详情"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    log = db.logs.find_one({"_id": ObjectId(log_id)})
    if not log:
        raise HTTPException(status_code=404, detail="日志未找到")
    
    return log

@router.delete("/logs/{log_id}")
async def delete_log(
    log_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """删除日志"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    result = db.logs.delete_one({"_id": ObjectId(log_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="日志未找到")
    
    return {"message": "日志已删除"}

@router.get("/logs/stats")
async def get_log_stats(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取日志统计信息"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 按级别统计
    level_stats = list(db.logs.aggregate([
        {"$group": {"_id": "$level", "count": {"$sum": 1}}}
    ]))
    
    # 按模块统计
    module_stats = list(db.logs.aggregate([
        {"$group": {"_id": "$module", "count": {"$sum": 1}}}
    ]))
    
    # 按操作统计
    action_stats = list(db.logs.aggregate([
        {"$group": {"_id": "$action", "count": {"$sum": 1}}}
    ]))
    
    # 最近24小时日志数量
    last_24h = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    last_24h_count = db.logs.count_documents({"created_at": {"$gte": last_24h}})
    
    return {
        "level_stats": level_stats,
        "module_stats": module_stats,
        "action_stats": action_stats,
        "last_24h_count": last_24h_count
    } 