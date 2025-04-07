from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class Subscription(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    tool_id: str
    notify_on_updates: bool = True
    notify_on_comments: bool = False
    notify_on_ratings: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class SubscriptionCreate(BaseModel):
    tool_id: str
    notify_on_updates: bool = True
    notify_on_comments: bool = False
    notify_on_ratings: bool = False

class SubscriptionUpdate(BaseModel):
    notify_on_updates: Optional[bool] = None
    notify_on_comments: Optional[bool] = None
    notify_on_ratings: Optional[bool] = None 