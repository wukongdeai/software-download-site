from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.version import Version, VersionCreate, VersionUpdate
from ..models.user import User
from ..auth import get_current_user, is_admin
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/tools/{tool_id}/versions", response_model=Version)
async def create_version(
    tool_id: str,
    version: VersionCreate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """创建新版本"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查工具是否存在
    tool = db.tools.find_one({"_id": ObjectId(tool_id)})
    if not tool:
        raise HTTPException(status_code=404, detail="工具未找到")
    
    # 检查版本号是否已存在
    existing_version = db.versions.find_one({
        "tool_id": tool_id,
        "version_number": version.version_number
    })
    if existing_version:
        raise HTTPException(status_code=400, detail="版本号已存在")
    
    version_data = version.dict()
    version_data["tool_id"] = tool_id
    version_data["release_date"] = datetime.utcnow()
    
    result = db.versions.insert_one(version_data)
    version_data["id"] = str(result.inserted_id)
    
    return version_data

@router.get("/tools/{tool_id}/versions", response_model=List[Version])
async def get_versions(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取工具的所有版本"""
    versions = list(db.versions.find({"tool_id": tool_id}).sort("release_date", -1))
    return versions

@router.get("/tools/{tool_id}/versions/{version_id}", response_model=Version)
async def get_version(
    tool_id: str,
    version_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取特定版本详情"""
    version = db.versions.find_one({
        "_id": ObjectId(version_id),
        "tool_id": tool_id
    })
    if not version:
        raise HTTPException(status_code=404, detail="版本未找到")
    
    return version

@router.put("/tools/{tool_id}/versions/{version_id}", response_model=Version)
async def update_version(
    tool_id: str,
    version_id: str,
    version_update: VersionUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """更新版本信息"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    version = db.versions.find_one({
        "_id": ObjectId(version_id),
        "tool_id": tool_id
    })
    if not version:
        raise HTTPException(status_code=404, detail="版本未找到")
    
    update_data = version_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    db.versions.update_one(
        {"_id": ObjectId(version_id)},
        {"$set": update_data}
    )
    
    updated_version = db.versions.find_one({"_id": ObjectId(version_id)})
    return updated_version

@router.delete("/tools/{tool_id}/versions/{version_id}")
async def delete_version(
    tool_id: str,
    version_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """删除版本"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    result = db.versions.delete_one({
        "_id": ObjectId(version_id),
        "tool_id": tool_id
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="版本未找到")
    
    return {"message": "版本已删除"}

@router.get("/tools/{tool_id}/versions/latest", response_model=Version)
async def get_latest_version(
    tool_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    """获取最新稳定版本"""
    version = db.versions.find_one(
        {"tool_id": tool_id, "is_stable": True},
        sort=[("release_date", -1)]
    )
    if not version:
        raise HTTPException(status_code=404, detail="未找到稳定版本")
    
    return version 