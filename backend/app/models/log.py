from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class Log(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    level: str  # INFO, WARNING, ERROR, DEBUG
    module: str
    action: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    message: str
    details: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class LogQuery(BaseModel):
    level: Optional[str] = None
    module: Optional[str] = None
    action: Optional[str] = None
    user_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    skip: int = 0
    limit: int = 100 