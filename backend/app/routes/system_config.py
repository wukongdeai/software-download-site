from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from ..models.system_config import SystemConfig
from ..models.user import User
from ..auth import get_current_user
from ..database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/configs", response_model=SystemConfig)
async def create_config(
    config: SystemConfig,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查配置键是否已存在
    existing_config = db.system_configs.find_one({"key": config.key})
    if existing_config:
        raise HTTPException(status_code=400, detail="配置键已存在")
    
    # 创建配置
    result = db.system_configs.insert_one(config.dict(exclude={"id"}))
    config.id = str(result.inserted_id)
    
    return config

@router.get("/configs", response_model=List[SystemConfig])
async def get_configs(
    current_user: User = Depends(get_current_user),
    db = Depends(get_database),
    skip: int = 0,
    limit: int = 100
):
    # 非管理员只能查看公开配置
    if not current_user.is_admin:
        configs = list(
            db.system_configs.find({"is_public": True})
            .sort("key", 1)
            .skip(skip)
            .limit(limit)
        )
    else:
        configs = list(
            db.system_configs.find()
            .sort("key", 1)
            .skip(skip)
            .limit(limit)
        )
    
    return configs

@router.get("/configs/{config_key}", response_model=SystemConfig)
async def get_config(
    config_key: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    config = db.system_configs.find_one({"key": config_key})
    if not config:
        raise HTTPException(status_code=404, detail="配置未找到")
    
    # 非管理员只能查看公开配置
    if not current_user.is_admin and not config.get("is_public", False):
        raise HTTPException(status_code=403, detail="无权访问此配置")
    
    return config

@router.put("/configs/{config_key}", response_model=SystemConfig)
async def update_config(
    config_key: str,
    config: SystemConfig,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查配置是否存在
    existing_config = db.system_configs.find_one({"key": config_key})
    if not existing_config:
        raise HTTPException(status_code=404, detail="配置未找到")
    
    # 更新配置
    config_dict = config.dict(exclude={"id"})
    config_dict["updated_at"] = datetime.utcnow()
    
    db.system_configs.update_one(
        {"key": config_key},
        {"$set": config_dict}
    )
    
    return {**config_dict, "id": str(existing_config["_id"])}

@router.delete("/configs/{config_key}")
async def delete_config(
    config_key: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 检查配置是否存在
    config = db.system_configs.find_one({"key": config_key})
    if not config:
        raise HTTPException(status_code=404, detail="配置未找到")
    
    # 删除配置
    db.system_configs.delete_one({"key": config_key})
    
    return {"message": "配置已删除"}

@router.get("/configs/batch", response_model=List[SystemConfig])
async def get_batch_configs(
    keys: List[str],
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    # 非管理员只能查看公开配置
    if not current_user.is_admin:
        configs = list(
            db.system_configs.find({
                "key": {"$in": keys},
                "is_public": True
            })
        )
    else:
        configs = list(
            db.system_configs.find({
                "key": {"$in": keys}
            })
        )
    
    return configs 