from sqlalchemy import Column, String
from app.database import Base
from pydantic import BaseModel
from typing import Literal

# SQLAlchemy model
class UserDB(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # nurse, admin, signage

# Pydantic model
class User(BaseModel):
    username: str
    role: Literal["nurse", "admin", "signage"]

    class Config:
        from_attributes = True
