from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserRequest, UserLoginRequest, TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from src.users.schemas import UserResponse
from .services import create_user, login_user, refresh_access_token, RefreshTokenRequest, forgot_password, reset_password
from ..db.session import get_db

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", response_model=UserResponse)
def register( user: UserRequest,db: Session = Depends(get_db)):
    return create_user(user, db)

@auth_router.post("/login", response_model=TokenResponse)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(user, db)

@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(token_data: RefreshTokenRequest):
    return refresh_access_token(token_data)

@auth_router.post("/forgot-password")
def forgot_password_endpoint(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(request, db)

@auth_router.post("/reset-password")
def reset_password_endpoint(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(request, db)