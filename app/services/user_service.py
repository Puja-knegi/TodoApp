from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.utils.hashing import hash_password
from app.db.session import get_db

def create_user(
        user_data: UserCreate, 
        db: Session= Depends(get_db)
 ) -> User:
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        email=user_data.email, 
        username=user_data.username,
        hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
