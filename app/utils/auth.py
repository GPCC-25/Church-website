from datetime import datetime, timedelta
from jose import jwt, JWTError
from bson import ObjectId
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.member_model import Member
import os
import logging

logger = logging.getLogger(__name__)


SECRET_KEY = os.getenv("Secret_ket", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user from JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        logger.debug(f"Authenticating user ID: {user_id}")
        user = await Member.get(ObjectId(user_id)
                                )
        if user is None:
            logger.warning(f"User not found: {user_id}")
            raise credentials_exception
    
        user_dict = user.dict()
        user_dict["id"] = str(user_dict["id"])
        user_dict.pop("password_hash", None)  
        return user
    


    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
    
    except Exception as e:
        logger.exception(f"Unexpected error in get_current_user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error"
        )
    



async def get_current_active_user(current_user: Member = Depends(get_current_user)):
    """Ensure the current user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user



def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)