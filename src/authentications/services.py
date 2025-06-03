from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import UserRequest, UserLoginRequest
from .user import User
from .hashing import hash_password, verify_password
from ..db.session import get_db

def create_user(user_data: UserRequest, db: Session= Depends(get_db)) -> User:    
    existing_email = db.query(User).filter(User.email == user_data.email).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email, 
        username=user_data.username,
        hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(user_data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return user