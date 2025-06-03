from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]