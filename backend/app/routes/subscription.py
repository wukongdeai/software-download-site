from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tools/{tool_id}/subscribe", response_model=Subscription)
async def create_subscription(
    tool_id: str,
    subscription: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """订阅工具"""
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 检查是否已订阅
    existing_subscription = db.subscriptions.find_one({
        "user_id": str(current_user.id),
        "tool_id": tool_id
    })
    if existing_subscription:
        raise HTTPException(status_code=400, detail="已订阅该工具")
    
    subscription_data = subscription.dict()
    subscription_data["user_id"] = str(current_user.id)
    subscription_data["tool_id"] = tool_id
    
    result = db.subscriptions.insert_one(subscription_data)
    subscription_data["id"] = str(result.inserted_id)
    
    return subscription_data

@router.get("/tools/{tool_id}/subscriptions", response_model=List[Subscription])
async def get_tool_subscriptions(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取工具的订阅列表"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    subscriptions = list(db.subscriptions.find({"tool_id": tool_id}))
    return subscriptions

@router.get("/users/subscriptions", response_model=List[Subscription])
async def get_user_subscriptions(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取用户的订阅列表"""
    subscriptions = list(db.subscriptions.find({"user_id": str(current_user.id)}))
    return subscriptions

@router.put("/tools/{tool_id}/subscriptions/{subscription_id}", response_model=Subscription)
async def update_subscription(
    tool_id: str,
    subscription_id: str,
    subscription_update: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """更新订阅设置"""
    subscription = db.subscriptions.find_one({
        "_id": ObjectId(subscription_id),
        "tool_id": tool_id,
        "user_id": str(current_user.id)
    })
    if not subscription:
        raise HTTPException(status_code=404, detail="订阅未找到")
    
    update_data = subscription_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    db.subscriptions.update_one(
        {"_id": ObjectId(subscription_id)},
        {"$set": update_data}
    )
    
    updated_subscription = db.subscriptions.find_one({"_id": ObjectId(subscription_id)})
    return updated_subscription

@router.delete("/tools/{tool_id}/subscriptions/{subscription_id}")
async def delete_subscription(
    tool_id: str,
    subscription_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """取消订阅"""
    subscription = db.subscriptions.find_one({
        "_id": ObjectId(subscription_id),
        "tool_id": tool_id,
        "user_id": str(current_user.id)
    })
    if not subscription:
        raise HTTPException(status_code=404, detail="订阅未找到")
    
    db.subscriptions.delete_one({"_id": ObjectId(subscription_id)})
    return {"message": "已取消订阅"}

@router.get("/tools/{tool_id}/subscribers/count")
async def get_subscriber_count(
    tool_id: str,
    db = Depends(get_database)
):
    """获取工具的订阅者数量"""
    count = db.subscriptions.count_documents({"tool_id": tool_id})
    return {"count": count} 