import asyncio, secrets, string
from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
from pydantic import EmailStr

from .jwt_methods import get_current_user
from .redis_client import redis_client
from src.utils.email_utils import send_email_async
from ..accounts.user_roles import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp(n=6):
    return ''.join(secrets.choice(string.digits) for _ in range(n))

async def send_verification_email(user_email: str):
    otp = generate_otp()
    await redis_client.setex(f"otp:{user_email}", 900, otp)
    subject = "Verify your account"
    body = f"Your OTP is {otp}. It expires in 15 minutes."
    await send_email_async(user_email, subject, body)


async def verify_otp(user_email: EmailStr, otp: str) -> bool:
    key = f"otp:{user_email}"
    stored_otp = await redis_client.get(key)
    if not stored_otp:
        return False
    if stored_otp != otp:
        return False

    await redis_client.delete(key)
    return True

async def delete_otp_from_redis(user_email: str):
    key = f"otp:{user_email}"
    deleted_count = await redis_client.delete(key)
    return deleted_count > 0

def get_current_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user