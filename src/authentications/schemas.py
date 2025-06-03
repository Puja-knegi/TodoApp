from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True