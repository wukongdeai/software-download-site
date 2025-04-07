from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.tutorial import Tutorial
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/tools/{tool_id}/tutorials", response_model=List[Tutorial])
async def get_tool_tutorials(
    tool_id: str,
    db = Depends(get_database)
):
    tutorials = list(db.tutorials.find({"tool_id": tool_id}))
    return tutorials

@router.post("/tools/{tool_id}/tutorials", response_model=Tutorial)
async def create_tutorial(
    tool_id: str,
    tutorial: Tutorial,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 设置作者ID
    tutorial.author_id = str(current_user.id)
    tutorial.tool_id = tool_id
    
    # 插入教程
    result = db.tutorials.insert_one(tutorial.dict(exclude={"id"}))
    tutorial.id = str(result.inserted_id)
    
    return tutorial

@router.put("/tutorials/{tutorial_id}", response_model=Tutorial)
async def update_tutorial(
    tutorial_id: str,
    tutorial: Tutorial,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查教程是否存在
    existing_tutorial = db.tutorials.find_one({"_id": ObjectId(tutorial_id)})
    if not existing_tutorial:
        raise HTTPException(status_code=404, detail="教程未找到")
    
    # 检查是否是作者
    if existing_tutorial["author_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权修改此教程")
    
    # 更新教程
    tutorial_dict = tutorial.dict(exclude={"id"})
    tutorial_dict["updated_at"] = datetime.utcnow()
    
    db.tutorials.update_one(
        {"_id": ObjectId(tutorial_id)},
        {"$set": tutorial_dict}
    )
    
    return {**tutorial_dict, "id": tutorial_id}

@router.delete("/tutorials/{tutorial_id}")
async def delete_tutorial(
    tutorial_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 检查教程是否存在
    tutorial = db.tutorials.find_one({"_id": ObjectId(tutorial_id)})
    if not tutorial:
        raise HTTPException(status_code=404, detail="教程未找到")
    
    # 检查是否是作者
    if tutorial["author_id"] != str(current_user.id):
        raise HTTPException(status_code=403, detail="无权删除此教程")
    
    # 删除教程
    db.tutorials.delete_one({"_id": ObjectId(tutorial_id)})
    
    return {"message": "教程已删除"} 