from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field
from bson import ObjectId

class ToolStatistics(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tool_id: str
    view_count: int = 0
    favorite_count: int = 0
    rating_count: int = 0
    average_rating: float = 0.0
    comment_count: int = 0
    daily_stats: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class UserStatistics(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    view_count: int = 0
    favorite_count: int = 0
    rating_count: int = 0
    comment_count: int = 0
    daily_stats: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        } 