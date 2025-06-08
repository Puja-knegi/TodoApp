from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserResponse, UserListResponse
from .services import get_all_users, get_user_by_email
from src.db.session import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.authentications.hashing import verify_token

users_router = APIRouter(
    tags=["users"]
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token, is_refresh=False)
    return payload

@users_router.get("/", response_model=UserListResponse)
def list_users(db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    return get_all_users(db)

@users_router.get("/{email}/", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db),  user: dict = Depends(get_current_user)):
    return get_user_by_email(email, db)