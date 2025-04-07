from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.permission import Permission, Role
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# 权限管理
@router.post("/permissions", response_model=Permission)
async def create_permission(
    permission: Permission,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查权限编码是否已存在
    existing_permission = db.permissions.find_one({"code": permission.code})
    if existing_permission:
        raise HTTPException(status_code=400, detail="权限编码已存在")
    
    # 检查父权限是否存在
    if permission.parent_id:
        parent_permission = db.permissions.find_one({"_id": ObjectId(permission.parent_id)})
        if not parent_permission:
            raise HTTPException(status_code=400, detail="父权限不存在")
        permission.level = parent_permission["level"] + 1
    
    # 创建权限
    result = db.permissions.insert_one(permission.dict(exclude={"id"}))
    permission.id = str(result.inserted_id)
    
    return permission

@router.get("/permissions", response_model=List[Permission])
async def get_permissions(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    permissions = list(
        db.permissions.find()
        .sort("level", 1)
        .skip(skip)
        .limit(limit)
    )
    
    return permissions

@router.get("/permissions/{permission_id}", response_model=Permission)
async def get_permission(
    permission_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    permission = db.permissions.find_one({"_id": ObjectId(permission_id)})
    if not permission:
        raise HTTPException(status_code=404, detail="权限未找到")
    
    return permission

@router.put("/permissions/{permission_id}", response_model=Permission)
async def update_permission(
    permission_id: str,
    permission: Permission,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查权限是否存在
    existing_permission = db.permissions.find_one({"_id": ObjectId(permission_id)})
    if not existing_permission:
        raise HTTPException(status_code=404, detail="权限未找到")
    
    # 检查权限编码是否与其他权限重复
    if permission.code != existing_permission["code"]:
        duplicate_permission = db.permissions.find_one({
            "code": permission.code,
            "_id": {"$ne": ObjectId(permission_id)}
        })
        if duplicate_permission:
            raise HTTPException(status_code=400, detail="权限编码已存在")
    
    # 检查父权限是否存在
    if permission.parent_id:
        parent_permission = db.permissions.find_one({"_id": ObjectId(permission.parent_id)})
        if not parent_permission:
            raise HTTPException(status_code=400, detail="父权限不存在")
        permission.level = parent_permission["level"] + 1
    
    # 更新权限
    permission_dict = permission.dict(exclude={"id"})
    permission_dict["updated_at"] = datetime.utcnow()
    
    db.permissions.update_one(
        {"_id": ObjectId(permission_id)},
        {"$set": permission_dict}
    )
    
    return {**permission_dict, "id": permission_id}

@router.delete("/permissions/{permission_id}")
async def delete_permission(
    permission_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查权限是否存在
    permission = db.permissions.find_one({"_id": ObjectId(permission_id)})
    if not permission:
        raise HTTPException(status_code=404, detail="权限未找到")
    
    # 检查是否有子权限
    child_count = db.permissions.count_documents({"parent_id": permission_id})
    if child_count > 0:
        raise HTTPException(status_code=400, detail="存在子权限，无法删除")
    
    # 检查是否有角色使用此权限
    role_count = db.roles.count_documents({"permissions": permission_id})
    if role_count > 0:
        raise HTTPException(status_code=400, detail="有角色使用此权限，无法删除")
    
    # 删除权限
    db.permissions.delete_one({"_id": ObjectId(permission_id)})
    
    return {"message": "权限已删除"}

# 角色管理
@router.post("/roles", response_model=Role)
async def create_role(
    role: Role,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查角色编码是否已存在
    existing_role = db.roles.find_one({"code": role.code})
    if existing_role:
        raise HTTPException(status_code=400, detail="角色编码已存在")
    
    # 检查权限是否存在
    for permission_id in role.permissions:
        permission = db.permissions.find_one({"_id": ObjectId(permission_id)})
        if not permission:
            raise HTTPException(status_code=400, detail=f"权限 {permission_id} 不存在")
    
    # 创建角色
    result = db.roles.insert_one(role.dict(exclude={"id"}))
    role.id = str(result.inserted_id)
    
    return role

@router.get("/roles", response_model=List[Role])
async def get_roles(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    roles = list(
        db.roles.find()
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    
    return roles

@router.get("/roles/{role_id}", response_model=Role)
async def get_role(
    role_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    role = db.roles.find_one({"_id": ObjectId(role_id)})
    if not role:
        raise HTTPException(status_code=404, detail="角色未找到")
    
    return role

@router.put("/roles/{role_id}", response_model=Role)
async def update_role(
    role_id: str,
    role: Role,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查角色是否存在
    existing_role = db.roles.find_one({"_id": ObjectId(role_id)})
    if not existing_role:
        raise HTTPException(status_code=404, detail="角色未找到")
    
    # 检查角色编码是否与其他角色重复
    if role.code != existing_role["code"]:
        duplicate_role = db.roles.find_one({
            "code": role.code,
            "_id": {"$ne": ObjectId(role_id)}
        })
        if duplicate_role:
            raise HTTPException(status_code=400, detail="角色编码已存在")
    
    # 检查权限是否存在
    for permission_id in role.permissions:
        permission = db.permissions.find_one({"_id": ObjectId(permission_id)})
        if not permission:
            raise HTTPException(status_code=400, detail=f"权限 {permission_id} 不存在")
    
    # 更新角色
    role_dict = role.dict(exclude={"id"})
    role_dict["updated_at"] = datetime.utcnow()
    
    db.roles.update_one(
        {"_id": ObjectId(role_id)},
        {"$set": role_dict}
    )
    
    return {**role_dict, "id": role_id}

@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查角色是否存在
    role = db.roles.find_one({"_id": ObjectId(role_id)})
    if not role:
        raise HTTPException(status_code=404, detail="角色未找到")
    
    # 检查是否有用户使用此角色
    user_count = db.users.count_documents({"role_id": role_id})
    if user_count > 0:
        raise HTTPException(status_code=400, detail="有用户使用此角色，无法删除")
    
    # 删除角色
    db.roles.delete_one({"_id": ObjectId(role_id)})
    
    return {"message": "角色已删除"} 