from sqlalchemy import Column, String
from datetime import datetime
from db.session import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()