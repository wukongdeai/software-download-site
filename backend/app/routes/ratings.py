from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..models.rating import Rating
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/tools/{tool_id}/rating")
async def get_tool_rating(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 获取工具的所有评分
    ratings = list(db.ratings.find({"tool_id": tool_id}))
    
    # 计算平均评分
    total_ratings = len(ratings)
    if total_ratings == 0:
        return {
            "average_rating": 0,
            "total_ratings": 0,
            "user_rating": None
        }
    
    average_rating = sum(rating["rating"] for rating in ratings) / total_ratings
    
    # 获取当前用户的评分
    user_rating = db.ratings.find_one({
        "tool_id": tool_id,
        "user_id": str(current_user.id)
    })
    
    return {
        "average_rating": round(average_rating, 1),
        "total_ratings": total_ratings,
        "user_rating": user_rating["rating"] if user_rating else None
    }

@router.post("/tools/{tool_id}/rating")
async def rate_tool(
    tool_id: str,
    rating_data: Dict[str, int],
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 验证评分值
    rating = rating_data.get("rating")
    if not rating or not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="评分必须在1到5之间")
    
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 更新或创建评分
    db.ratings.update_one(
        {
            "tool_id": tool_id,
            "user_id": str(current_user.id)
        },
        {
            "$set": {
                "rating": rating,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    return {"message": "评分成功"} 