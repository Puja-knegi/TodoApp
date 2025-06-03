from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .user import User
from .schemas import UserListResponse

def get_all_users(db: Session):
    users = db.query(User).all()
    return UserListResponse(users=users)

def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user