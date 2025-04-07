from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.models.tool import Tool, ToolCreate, ToolUpdate
from app.database import get_database
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[Tool])
async def get_tools(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None
):
    db = get_database()
    query = {"is_active": True}
    
    if category:
        query["category"] = category
    if is_featured is not None:
        query["is_featured"] = is_featured
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$regex": search, "$options": "i"}}
        ]
    
    tools = await db.tools.find(query).skip(skip).limit(limit).to_list(length=limit)
    return tools

@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: str):
    db = get_database()
    if (tool := await db.tools.find_one({"_id": ObjectId(tool_id)})) is not None:
        return tool
    raise HTTPException(status_code=404, detail="Tool not found")

@router.post("/", response_model=Tool)
async def create_tool(tool: ToolCreate):
    db = get_database()
    tool_dict = tool.dict()
    tool_dict["created_at"] = datetime.utcnow()
    tool_dict["updated_at"] = datetime.utcnow()
    
    result = await db.tools.insert_one(tool_dict)
    created_tool = await db.tools.find_one({"_id": result.inserted_id})
    return created_tool

@router.put("/{tool_id}", response_model=Tool)
async def update_tool(tool_id: str, tool: ToolUpdate):
    db = get_database()
    tool_dict = {k: v for k, v in tool.dict().items() if v is not None}
    tool_dict["updated_at"] = datetime.utcnow()
    
    if len(tool_dict) >= 1:
        update_result = await db.tools.update_one(
            {"_id": ObjectId(tool_id)},
            {"$set": tool_dict}
        )
        
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Tool not found")
    
    if (updated_tool := await db.tools.find_one({"_id": ObjectId(tool_id)})) is not None:
        return updated_tool
    raise HTTPException(status_code=404, detail="Tool not found")

@router.delete("/{tool_id}")
async def delete_tool(tool_id: str):
    db = get_database()
    delete_result = await db.tools.delete_one({"_id": ObjectId(tool_id)})
    
    if delete_result.deleted_count == 1:
        return {"message": "Tool deleted successfully"}
    raise HTTPException(status_code=404, detail="Tool not found") 