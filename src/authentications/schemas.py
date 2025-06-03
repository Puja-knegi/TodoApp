from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenBase(BaseModel):
    token_type: str
    access_token: str

class TokenResponse(TokenBase):
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
