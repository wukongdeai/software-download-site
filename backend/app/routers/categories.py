from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_database
from bson import ObjectId

router = APIRouter()

class Category(BaseModel):
    name: str
    description: str
    icon: str
    is_active: bool = True

class CategoryInDB(Category):
    id: str
    created_at: datetime
    updated_at: datetime

@router.get("/", response_model=List[CategoryInDB])
async def get_categories():
    db = get_database()
    categories = await db.categories.find({"is_active": True}).to_list(length=100)
    return categories

@router.get("/{category_id}", response_model=CategoryInDB)
async def get_category(category_id: str):
    db = get_database()
    if (category := await db.categories.find_one({"_id": ObjectId(category_id)})) is not None:
        return category
    raise HTTPException(status_code=404, detail="Category not found")

@router.post("/", response_model=CategoryInDB)
async def create_category(category: Category):
    db = get_database()
    category_dict = category.dict()
    category_dict["created_at"] = datetime.utcnow()
    category_dict["updated_at"] = datetime.utcnow()
    
    result = await db.categories.insert_one(category_dict)
    created_category = await db.categories.find_one({"_id": result.inserted_id})
    return created_category

@router.put("/{category_id}", response_model=CategoryInDB)
async def update_category(category_id: str, category: Category):
    db = get_database()
    category_dict = category.dict()
    category_dict["updated_at"] = datetime.utcnow()
    
    update_result = await db.categories.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category_dict}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if (updated_category := await db.categories.find_one({"_id": ObjectId(category_id)})) is not None:
        return updated_category
    raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    db = get_database()
    delete_result = await db.categories.delete_one({"_id": ObjectId(category_id)})
    
    if delete_result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found") 