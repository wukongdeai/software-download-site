from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.recommendation import Recommendation
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/recommendations", response_model=List[Recommendation])
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database),
    limit: int = 10
):
    # 获取用户的收藏工具
    favorites = list(db.favorites.find({"user_id": str(current_user.id)}))
    favorite_tool_ids = [favorite["tool_id"] for favorite in favorites]
    
    # 获取用户的评分工具
    ratings = list(db.ratings.find({"user_id": str(current_user.id)}))
    rated_tool_ids = [rating["tool_id"] for rating in ratings]
    
    # 获取用户浏览过的工具
    viewed_tools = list(db.user_views.find({"user_id": str(current_user.id)}))
    viewed_tool_ids = [view["tool_id"] for view in viewed_tools]
    
    # 获取所有相关工具
    related_tools = []
    
    # 基于收藏的工具推荐
    for tool_id in favorite_tool_ids:
        tool = db.tools.find_one({"_id": ObjectId(tool_id)})
        if tool and tool.get("related_tools"):
            related_tools.extend(tool["related_tools"])
    
    # 基于评分的工具推荐
    for tool_id in rated_tool_ids:
        tool = db.tools.find_one({"_id": ObjectId(tool_id)})
        if tool and tool.get("related_tools"):
            related_tools.extend(tool["related_tools"])
    
    # 基于浏览历史的工具推荐
    for tool_id in viewed_tool_ids:
        tool = db.tools.find_one({"_id": ObjectId(tool_id)})
        if tool and tool.get("related_tools"):
            related_tools.extend(tool["related_tools"])
    
    # 去重并计算推荐分数
    tool_scores = {}
    for tool in related_tools:
        tool_id = str(tool["_id"])
        if tool_id not in tool_scores:
            tool_scores[tool_id] = 0
        tool_scores[tool_id] += 1
    
    # 排除用户已经收藏、评分或浏览过的工具
    excluded_tool_ids = set(favorite_tool_ids + rated_tool_ids + viewed_tool_ids)
    recommended_tools = [
        {
            "user_id": str(current_user.id),
            "tool_id": tool_id,
            "score": score
        }
        for tool_id, score in tool_scores.items()
        if tool_id not in excluded_tool_ids
    ]
    
    # 按分数排序并限制数量
    recommended_tools.sort(key=lambda x: x["score"], reverse=True)
    recommended_tools = recommended_tools[:limit]
    
    return recommended_tools

@router.get("/tools/{tool_id}/recommendations", response_model=List[Recommendation])
async def get_tool_recommendations(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database),
    limit: int = 5
):
    # 获取工具信息
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 获取相关工具
    related_tools = tool.get("related_tools", [])
    
    # 计算推荐分数
    recommended_tools = []
    for related_tool in related_tools:
        # 计算相似度分数（这里简单使用1作为基础分数）
        score = 1.0
        
        # 如果用户已经收藏过该工具，增加分数
        favorite = db.favorites.find_one({
            "user_id": str(current_user.id),
            "tool_id": str(related_tool["_id"])
        })
        if favorite:
            score += 0.5
        
        # 如果用户已经评分过该工具，增加分数
        rating = db.ratings.find_one({
            "user_id": str(current_user.id),
            "tool_id": str(related_tool["_id"])
        })
        if rating:
            score += 0.3
        
        recommended_tools.append({
            "user_id": str(current_user.id),
            "tool_id": str(related_tool["_id"]),
            "score": score
        })
    
    # 按分数排序并限制数量
    recommended_tools.sort(key=lambda x: x["score"], reverse=True)
    recommended_tools = recommended_tools[:limit]
    
    return recommended_tools 