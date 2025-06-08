import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

OTP_SECRET_KEY = os.getenv("OTP_SECRET_KEY")
OTP_EXPIRE_MINUTES = int(os.getenv("OTP_EXPIRE_MINUTES", "10"))
OTP_LENGTH = int(os.getenv("OTP_LENGTH", "6"))

otp_storage = {}

def generate_otp(email: str) -> str:
    otp = ''.join([str(random.randint(0, 9)) for _ in range(OTP_LENGTH)])
    expires_at = datetime.now() + timedelta(minutes=OTP_EXPIRE_MINUTES)
    
    otp_storage[email] = {
        "otp": otp,
        "expires_at": expires_at
    }
    
    return otp

def verify_otp(email: str, otp: str) -> bool:
    stored_data = otp_storage.get(email)
    
    if not stored_data:
        return False
        
    if datetime.now() > stored_data["expires_at"]:
        del otp_storage[email]
        return False
        
    if stored_data["otp"] != otp:
        return False
    
    del otp_storage[email]
    return True