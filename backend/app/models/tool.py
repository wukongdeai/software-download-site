from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ToolBase(BaseModel):
    name: str
    description: str
    url: str
    category: str
    subcategory: Optional[str] = None
    tags: List[str] = []
    icon: Optional[str] = None
    is_free: bool = True
    is_featured: bool = False
    rating: float = 0.0
    views: int = 0
    likes: int = 0
    is_active: bool = True

class ToolCreate(ToolBase):
    pass

class ToolUpdate(ToolBase):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None

class ToolInDB(ToolBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

class Tool(ToolInDB):
    class Config:
        allow_population_by_field_name = True 