from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class Share(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tool_id: str
    user_id: str
    platform: str  # 分享平台：wechat, weibo, twitter, facebook等
    share_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class ShareCreate(BaseModel):
    tool_id: str
    platform: str
    share_url: str

class ShareStats(BaseModel):
    tool_id: str
    total_shares: int
    platform_stats: dict
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 