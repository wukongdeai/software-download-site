from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.search import SearchQuery, SearchResult
from ..database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/search", response_model=SearchResult)
async def search_tools(
    query: SearchQuery,
    db = Depends(get_database)
):
    # 构建查询条件
    search_filter = {}
    
    if query.keyword:
        search_filter["$or"] = [
            {"name": {"$regex": query.keyword, "$options": "i"}},
            {"description": {"$regex": query.keyword, "$options": "i"}},
            {"tags": {"$regex": query.keyword, "$options": "i"}}
        ]
    
    if query.category_id:
        search_filter["category_id"] = query.category_id
    
    if query.tags:
        search_filter["tags"] = {"$all": query.tags}
    
    if query.is_free is not None:
        search_filter["is_free"] = query.is_free
    
    # 构建排序条件
    sort_field = query.sort_by or "created_at"
    sort_order = -1 if query.sort_order == "desc" else 1
    sort_condition = [(sort_field, sort_order)]
    
    # 计算分页
    skip = (query.page - 1) * query.page_size
    limit = query.page_size
    
    # 执行查询
    total = db.tools.count_documents(search_filter)
    tools = list(
        db.tools.find(search_filter)
        .sort(sort_condition)
        .skip(skip)
        .limit(limit)
    )
    
    # 计算总页数
    total_pages = (total + query.page_size - 1) // query.page_size
    
    # 转换ObjectId为字符串
    for tool in tools:
        tool["_id"] = str(tool["_id"])
        if "category_id" in tool:
            tool["category_id"] = str(tool["category_id"])
    
    return {
        "total": total,
        "tools": tools,
        "page": query.page,
        "page_size": query.page_size,
        "total_pages": total_pages
    }

@router.get("/search/suggestions")
async def get_search_suggestions(
    keyword: str,
    db = Depends(get_database),
    limit: int = 5
):
    # 搜索工具名称
    tools = list(
        db.tools.find(
            {"name": {"$regex": keyword, "$options": "i"}},
            {"name": 1, "_id": 1}
        ).limit(limit)
    )
    
    # 搜索标签
    tags = list(
        db.tools.aggregate([
            {"$match": {"tags": {"$regex": keyword, "$options": "i"}}},
            {"$unwind": "$tags"},
            {"$match": {"tags": {"$regex": keyword, "$options": "i"}}},
            {"$group": {"_id": "$tags"}},
            {"$limit": limit}
        ])
    )
    
    # 转换ObjectId为字符串
    for tool in tools:
        tool["_id"] = str(tool["_id"])
    
    return {
        "tools": [{"id": tool["_id"], "name": tool["name"]} for tool in tools],
        "tags": [tag["_id"] for tag in tags]
    } 