import os
from datetime import datetime, timedelta
from fastapi import Response, Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt import PyJWTError
from src.db.database import get_db
from src.db.models import User

secret_key = os.getenv("SECRET_KEY")
access_token_expire_in_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
algorithm = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    expires_delta =  None
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=access_token_expire_in_minutes))
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    payload = jwt.decode(encoded_jwt, secret_key, algorithms=[algorithm])
    return encoded_jwt

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise Exception()
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user = await session.get(User, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
