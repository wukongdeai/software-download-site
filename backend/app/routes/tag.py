from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.tag import Tag
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tags", response_model=Tag)
async def create_tag(
    tag: Tag,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查标签名称是否已存在
    existing_tag = db.tags.find_one({"name": tag.name})
    if existing_tag:
        raise HTTPException(status_code=400, detail="标签名称已存在")
    
    # 创建标签
    result = db.tags.insert_one(tag.dict(exclude={"id"}))
    tag.id = str(result.inserted_id)
    
    return tag

@router.get("/tags", response_model=List[Tag])
async def get_tags(
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    tags = list(
        db.tags.find()
        .sort("tool_count", -1)
        .skip(skip)
        .limit(limit)
    )
    
    return tags

@router.get("/tags/{tag_id}", response_model=Tag)
async def get_tag(
    tag_id: str,
    db = Depends(get_database)
):
    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    
    return tag

@router.put("/tags/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: str,
    tag: Tag,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查标签是否存在
    existing_tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not existing_tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    
    # 检查标签名称是否与其他标签重复
    if tag.name != existing_tag["name"]:
        duplicate_tag = db.tags.find_one({
            "name": tag.name,
            "_id": {"$ne": ObjectId(tag_id)}
        })
        if duplicate_tag:
            raise HTTPException(status_code=400, detail="标签名称已存在")
    
    # 更新标签
    tag_dict = tag.dict(exclude={"id"})
    tag_dict["updated_at"] = datetime.utcnow()
    
    db.tags.update_one(
        {"_id": ObjectId(tag_id)},
        {"$set": tag_dict}
    )
    
    return {**tag_dict, "id": tag_id}

@router.delete("/tags/{tag_id}")
async def delete_tag(
    tag_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查标签是否存在
    tag = db.tags.find_one({"_id": ObjectId(tag_id)})
    if not tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    
    # 检查标签是否有关联的工具
    tool_count = db.tools.count_documents({"tags": tag_id})
    if tool_count > 0:
        raise HTTPException(status_code=400, detail="标签下存在工具，无法删除")
    
    # 删除标签
    db.tags.delete_one({"_id": ObjectId(tag_id)})
    
    return {"message": "标签已删除"}

@router.get("/tags/popular", response_model=List[Tag])
async def get_popular_tags(
    db = Depends(get_database),
    limit: int = 10
):
    tags = list(
        db.tags.find()
        .sort("tool_count", -1)
        .limit(limit)
    )
    
    return tags 