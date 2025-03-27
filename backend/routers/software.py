from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.software import Software, SoftwareCreate, SoftwareUpdate
from database import db
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Software])
async def get_software_list(
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = db.software.find(query).skip(skip).limit(limit)
    software_list = await cursor.to_list(length=limit)
    return software_list

@router.get("/{software_id}", response_model=Software)
async def get_software_detail(software_id: str):
    if not ObjectId.is_valid(software_id):
        raise HTTPException(status_code=400, detail="Invalid software ID")
    
    software = await db.software.find_one({"_id": ObjectId(software_id)})
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    return software

@router.post("/{software_id}/download")
async def increment_download_count(software_id: str):
    if not ObjectId.is_valid(software_id):
        raise HTTPException(status_code=400, detail="Invalid software ID")
    
    result = await db.software.update_one(
        {"_id": ObjectId(software_id)},
        {"$inc": {"download_count": 1}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Software not found")
    return {"message": "Download count incremented"} 