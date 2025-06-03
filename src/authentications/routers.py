from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserRequest, UserResponse, UserLoginRequest
from .services import create_user, login_user
from ..db.session import get_db

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register", response_model=UserResponse, status_code=201)
def register( user: UserRequest,db: Session = Depends(get_db)):
    return create_user(user, db)

@auth_router.post("/login", response_model=UserResponse)
def login(user: UserLoginRequest, db: Session = Depends(get_db)):
    return login_user(user, db)