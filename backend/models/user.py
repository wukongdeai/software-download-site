from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = datetime.utcnow()

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str 