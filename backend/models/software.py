from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class DownloadLink(BaseModel):
    platform: str  # 如：百度网盘、阿里云盘等
    url: str
    password: Optional[str] = None

class Version(BaseModel):
    version_number: str
    release_date: datetime
    file_size: str
    download_links: List[DownloadLink]
    md5: Optional[str] = None
    sha1: Optional[str] = None
    changelog: Optional[str] = None

class SoftwareBase(BaseModel):
    name: str
    description: str
    category: str
    icon_url: str
    versions: List[Version]
    download_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Software(SoftwareBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class SoftwareCreate(SoftwareBase):
    pass

class SoftwareUpdate(SoftwareBase):
    pass 