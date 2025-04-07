from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class Permission(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[str] = None
    level: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class Role(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    code: str
    description: Optional[str] = None
    permissions: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        } 