from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

class Version(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    tool_id: str
    version_number: str
    release_date: datetime
    changes: List[str]
    features: List[str]
    improvements: List[str]
    bug_fixes: List[str]
    is_stable: bool = True
    download_url: Optional[str] = None
    documentation_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class VersionCreate(BaseModel):
    tool_id: str
    version_number: str
    changes: List[str]
    features: List[str]
    improvements: List[str]
    bug_fixes: List[str]
    is_stable: bool = True
    download_url: Optional[str] = None
    documentation_url: Optional[str] = None

class VersionUpdate(BaseModel):
    version_number: Optional[str] = None
    changes: Optional[List[str]] = None
    features: Optional[List[str]] = None
    improvements: Optional[List[str]] = None
    bug_fixes: Optional[List[str]] = None
    is_stable: Optional[bool] = None
    download_url: Optional[str] = None
    documentation_url: Optional[str] = None 