from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.database import get_db, settings
from app.models.user import User, UserDB
from typing import Optional
from datetime import datetime, timedelta

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_initial_users(db: AsyncSession = Depends(get_db)):
    # Check if users exist
    result = await db.execute(text("SELECT username FROM users WHERE username IN ('admin', 'nurse', 'signage')"))
    existing_users = {row["username"] for row in result.mappings().all()}
    
    # Create default users if they don't exist
    default_users = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "nurse", "password": "nurse123", "role": "nurse"},
        {"username": "signage", "password": "signage123", "role": "signage"},
    ]
    
    for user in default_users:
        if user["username"] not in existing_users:
            hashed_password = pwd_context.hash(user["password"])
            db_user = UserDB(
                username=user["username"],
                hashed_password=hashed_password,
                role=user["role"]
            )
            db.add(db_user)
    await db.commit()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})
    user = result.mappings().first()
    if user is None:
        raise credentials_exception
    return User(**user)

def get_current_user_with_role(required_role: str):
    async def check_user_role(user: User = Depends(get_current_user)) -> User:
        if user.role != required_role and user.role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check_user_role
