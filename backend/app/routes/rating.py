from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.rating import Rating, RatingStats
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tools/{tool_id}/ratings", response_model=Rating)
async def create_rating(
    tool_id: str,
    rating: Rating,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 检查用户是否已经评分
    existing_rating = db.ratings.find_one({
        "tool_id": tool_id,
        "user_id": current_user.id
    })
    if existing_rating:
        raise HTTPException(status_code=400, detail="您已经评分过此工具")
    
    # 创建评分
    rating.tool_id = tool_id
    rating.user_id = current_user.id
    result = db.ratings.insert_one(rating.dict(exclude={"id"}))
    rating.id = str(result.inserted_id)
    
    # 更新评分统计
    await update_rating_stats(tool_id, db)
    
    return rating

@router.get("/tools/{tool_id}/ratings", response_model=List[Rating])
async def get_ratings(
    tool_id: str,
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    ratings = list(
        db.ratings.find({"tool_id": tool_id})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    
    return ratings

@router.get("/tools/{tool_id}/ratings/{rating_id}", response_model=Rating)
async def get_rating(
    tool_id: str,
    rating_id: str,
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    rating = db.ratings.find_one({
        "_id": ObjectId(rating_id),
        "tool_id": tool_id
    })
    if not rating:
        raise HTTPException(status_code=404, detail="评分未找到")
    
    return rating

@router.put("/tools/{tool_id}/ratings/{rating_id}", response_model=Rating)
async def update_rating(
    tool_id: str,
    rating_id: str,
    rating: Rating,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 检查评分是否存在
    existing_rating = db.ratings.find_one({
        "_id": ObjectId(rating_id),
        "tool_id": tool_id
    })
    if not existing_rating:
        raise HTTPException(status_code=404, detail="评分未找到")
    
    # 检查是否是评分作者或管理员
    if existing_rating["user_id"] != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权修改此评分")
    
    # 更新评分
    rating_dict = rating.dict(exclude={"id"})
    rating_dict["updated_at"] = datetime.utcnow()
    
    db.ratings.update_one(
        {"_id": ObjectId(rating_id)},
        {"$set": rating_dict}
    )
    
    # 更新评分统计
    await update_rating_stats(tool_id, db)
    
    return {**rating_dict, "id": rating_id}

@router.delete("/tools/{tool_id}/ratings/{rating_id}")
async def delete_rating(
    tool_id: str,
    rating_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 检查评分是否存在
    rating = db.ratings.find_one({
        "_id": ObjectId(rating_id),
        "tool_id": tool_id
    })
    if not rating:
        raise HTTPException(status_code=404, detail="评分未找到")
    
    # 检查是否是评分作者或管理员
    if rating["user_id"] != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="无权删除此评分")
    
    # 删除评分
    db.ratings.delete_one({"_id": ObjectId(rating_id)})
    
    # 更新评分统计
    await update_rating_stats(tool_id, db)
    
    return {"message": "评分已删除"}

@router.get("/tools/{tool_id}/ratings/stats", response_model=RatingStats)
async def get_rating_stats(
    tool_id: str,
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    stats = db.rating_stats.find_one({"tool_id": tool_id})
    if not stats:
        # 如果没有统计信息，创建新的
        stats = await update_rating_stats(tool_id, db)
    
    return stats

async def update_rating_stats(tool_id: str, db) -> RatingStats:
    # 获取所有评分
    ratings = list(db.ratings.find({"tool_id": tool_id}))
    
    # 计算统计信息
    total_ratings = len(ratings)
    if total_ratings == 0:
        average_score = 0
        score_distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        tag_stats = {}
    else:
        # 计算平均分
        total_score = sum(rating["score"] for rating in ratings)
        average_score = total_score / total_ratings
        
        # 计算分数分布
        score_distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        for rating in ratings:
            score = str(int(rating["score"]))
            score_distribution[score] += 1
        
        # 计算标签统计
        tag_stats = {}
        for rating in ratings:
            for tag in rating.get("tags", []):
                tag_stats[tag] = tag_stats.get(tag, 0) + 1
    
    # 创建或更新统计信息
    stats = RatingStats(
        tool_id=tool_id,
        average_score=average_score,
        total_ratings=total_ratings,
        score_distribution=score_distribution,
        tag_stats=tag_stats
    )
    
    db.rating_stats.update_one(
        {"tool_id": tool_id},
        {"$set": stats.dict(exclude={"id"})},
        upsert=True
    )
    
    return stats 