from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class Rating(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tool_id: str
    user_id: str
    score: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class RatingStats(BaseModel):
    tool_id: str
    average_score: float = 0
    total_ratings: int = 0
    score_distribution: dict = Field(default_factory=lambda: {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    })
    tag_stats: dict = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        } 