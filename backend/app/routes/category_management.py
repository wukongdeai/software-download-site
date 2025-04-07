from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.category_management import CategoryManagement
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/categories", response_model=CategoryManagement)
async def create_category(
    category: CategoryManagement,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查分类名称是否已存在
    existing_category = db.categories.find_one({"name": category.name})
    if existing_category:
        raise HTTPException(status_code=400, detail="分类名称已存在")
    
    # 创建分类
    result = db.categories.insert_one(category.dict(exclude={"id"}))
    category.id = str(result.inserted_id)
    
    return category

@router.get("/categories", response_model=List[CategoryManagement])
async def get_categories(
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    categories = list(
        db.categories.find()
        .sort("order", 1)
        .skip(skip)
        .limit(limit)
    )
    
    return categories

@router.get("/categories/{category_id}", response_model=CategoryManagement)
async def get_category(
    category_id: str,
    db = Depends(get_database)
):
    category = db.categories.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")
    
    return category

@router.put("/categories/{category_id}", response_model=CategoryManagement)
async def update_category(
    category_id: str,
    category: CategoryManagement,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查分类是否存在
    existing_category = db.categories.find_one({"_id": ObjectId(category_id)})
    if not existing_category:
        raise HTTPException(status_code=404, detail="分类未找到")
    
    # 检查分类名称是否与其他分类重复
    if category.name != existing_category["name"]:
        duplicate_category = db.categories.find_one({
            "name": category.name,
            "_id": {"$ne": ObjectId(category_id)}
        })
        if duplicate_category:
            raise HTTPException(status_code=400, detail="分类名称已存在")
    
    # 更新分类
    category_dict = category.dict(exclude={"id"})
    category_dict["updated_at"] = datetime.utcnow()
    
    db.categories.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category_dict}
    )
    
    return {**category_dict, "id": category_id}

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查分类是否存在
    category = db.categories.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="分类未找到")
    
    # 检查分类是否有关联的工具
    tool_count = db.tools.count_documents({"category_id": category_id})
    if tool_count > 0:
        raise HTTPException(status_code=400, detail="分类下存在工具，无法删除")
    
    # 删除分类
    db.categories.delete_one({"_id": ObjectId(category_id)})
    
    return {"message": "分类已删除"} 