from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_database
from app.routers.auth import get_current_user, User
from bson import ObjectId

router = APIRouter()

class UserUpdate(BaseModel):
    email: str
    is_active: bool = True

class UserInDB(User):
    id: str
    created_at: datetime

@router.get("/", response_model=List[UserInDB])
async def get_users(current_user: User = Depends(get_current_user)):
    db = get_database()
    users = await db.users.find().to_list(length=100)
    return users

@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    db = get_database()
    if (user := await db.users.find_one({"_id": ObjectId(user_id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    db = get_database()
    user_dict = user.dict()
    user_dict["updated_at"] = datetime.utcnow()
    
    update_result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_dict}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    if (updated_user := await db.users.find_one({"_id": ObjectId(user_id)})) is not None:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    db = get_database()
    delete_result = await db.users.delete_one({"_id": ObjectId(user_id)})
    
    if delete_result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found") 