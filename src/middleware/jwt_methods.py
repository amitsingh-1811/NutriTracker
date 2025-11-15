import os
from datetime import datetime, timedelta
from fastapi import Response
import jwt


secret_key = os.getenv("SECRET_KEY")
access_token_expire_in_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
algorithm = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    expires_delta =  None
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=access_token_expire_in_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt