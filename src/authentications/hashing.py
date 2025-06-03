import os
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("PASSWORD_HASH_SECRET_KEY", "")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    peppered_password = f"{password}{SECRET_KEY}"
    return pwd_context.hash(peppered_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered_password = f"{plain_password}{SECRET_KEY}"
    return pwd_context.verify(peppered_password, hashed_password)