from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import UserRequest, UserLoginRequest, TokenResponse, RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
from src.users.user import User
from .hashing import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from ..db.session import get_db
from .email_service import email_service
from .otp_service import generate_otp, verify_otp


def create_user(user_data: UserRequest, db: Session= Depends(get_db)) -> User:    
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    existing_username = db.query(User).filter(User.username == user_data.username).first()

    if existing_email: raise HTTPException(status_code=400, detail="Email already registered")
    if existing_username: raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email, 
        username=user_data.username,
        hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this email does not exist"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    return user

def login_user(user_data: UserLoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

def refresh_access_token(token_data: RefreshTokenRequest):
    payload = verify_token(token_data.refresh_token, is_refresh=True)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    new_access_token = create_access_token(data={"sub": payload.get("sub")})
    new_refresh_token = create_refresh_token(data={"sub": payload.get("sub")})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

def forgot_password(request: ForgotPasswordRequest, db: Session):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return {"message": "If the email exists, a password reset OTP has been sent"}

    otp_code = generate_otp(request.email)

    subject = "Password Reset OTP"
    body = f"""
    <html>
        <body>
            <p>Hello,</p>
            <p>Your password reset OTP is:</p>
            <p><strong>{otp_code}</strong></p>
            <p>This OTP is valid for 2 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
    </html>
    """
    email_service.send_email(request.email, subject, body)
    
    return {"message": "If the email exists, a password reset OTP has been sent"}

def reset_password(request: ResetPasswordRequest, db: Session):
    is_valid = verify_otp(request.email, request.otp)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
 
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    hashed_password = hash_password(request.new_password)

    user.hashed_password = hashed_password
    db.commit()
    
    return {"message": "Password reset successfully"}