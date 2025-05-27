from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user
from app.db.session import get_db
from app.models.user import User
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(User.email == user.email).first()
    
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(user, db)
