import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("PASSWORD_HASH_SECRET_KEY", "")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    peppered_password = f"{password}{SECRET_KEY}"
    return pwd_context.hash(peppered_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered_password = f"{plain_password}{SECRET_KEY}"
    return pwd_context.verify(peppered_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, is_refresh: bool = False):
    try:
        secret = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_SECRET_KEY
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None