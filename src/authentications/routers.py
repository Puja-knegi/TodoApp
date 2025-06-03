from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserRequest, UserLoginRequest, TokenResponse
from .services import create_user, login_user, refresh_access_token, RefreshTokenRequest
from ..db.session import get_db

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", response_model=TokenResponse)
def register( user: UserRequest,db: Session = Depends(get_db)):
    return create_user(user, db)

@auth_router.post("/login", response_model=TokenResponse)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(user, db)

@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(token_data: RefreshTokenRequest):
    return refresh_access_token(token_data)