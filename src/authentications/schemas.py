from pydantic import BaseModel, EmailStr, field_validator
import re

class UserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,64}$', v):
            raise ValueError(
                "Password must contain at least 8 digits one uppercase letter, "
                "one lowercase letter, one number and one special character"
            )
        return v

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
    
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

    @field_validator('new_password')
    def validate_password(cls, v):
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,64}$', v):
            raise ValueError(
                "Password must contain at least 8 digits one uppercase letter, "
                "one lowercase letter, one number and one special character"
            )
        return v