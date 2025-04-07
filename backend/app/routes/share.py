from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.share import Share, ShareCreate, ShareStats
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tools/{tool_id}/shares", response_model=Share)
async def create_share(
    tool_id: str,
    share: ShareCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """记录分享"""
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    share_data = share.dict()
    share_data["user_id"] = str(current_user.id)
    share_data["tool_id"] = tool_id
    
    result = db.shares.insert_one(share_data)
    share_data["id"] = str(result.inserted_id)
    
    # 更新分享统计
    await update_share_stats(tool_id, share.platform, db)
    
    return share_data

@router.get("/tools/{tool_id}/shares", response_model=List[Share])
async def get_tool_shares(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取工具的分享记录"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    shares = list(db.shares.find({"tool_id": tool_id}).sort("created_at", -1))
    return shares

@router.get("/tools/{tool_id}/shares/stats", response_model=ShareStats)
async def get_share_stats(
    tool_id: str,
    db = Depends(get_database)
):
    """获取工具的分享统计"""
    stats = db.share_stats.find_one({"tool_id": tool_id})
    if not stats:
        # 如果没有统计记录，创建一个新的
        stats = {
            "tool_id": tool_id,
            "total_shares": 0,
            "platform_stats": {}
        }
        db.share_stats.insert_one(stats)
    
    return stats

async def update_share_stats(tool_id: str, platform: str, db):
    """更新分享统计"""
    stats = db.share_stats.find_one({"tool_id": tool_id})
    if not stats:
        stats = {
            "tool_id": tool_id,
            "total_shares": 0,
            "platform_stats": {}
        }
        db.share_stats.insert_one(stats)
    
    # 更新总分享数
    total_shares = db.shares.count_documents({"tool_id": tool_id})
    
    # 更新平台统计
    platform_stats = {}
    for share in db.shares.find({"tool_id": tool_id}):
        platform = share["platform"]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    
    db.share_stats.update_one(
        {"tool_id": tool_id},
        {
            "$set": {
                "total_shares": total_shares,
                "platform_stats": platform_stats,
                "updated_at": datetime.utcnow()
            }
        }
    )

@router.get("/users/shares", response_model=List[Share])
async def get_user_shares(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取用户的分享记录"""
    shares = list(db.shares.find({"user_id": str(current_user.id)}).sort("created_at", -1))
    return shares 