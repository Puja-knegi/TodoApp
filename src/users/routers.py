from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserResponse, UserListResponse
from .services import get_all_users, get_user_by_email
from src.db.session import get_db

users_router = APIRouter(
    tags=["users"]
)

@users_router.get("/", response_model=UserListResponse)
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@users_router.get("/{email}/", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(email, db)