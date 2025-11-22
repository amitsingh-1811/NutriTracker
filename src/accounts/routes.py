import os

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from ..accounts.user_roles import UserRole
import asyncio

from src.db.models import User
from src.db.database import get_db
from .schemas import UserCreate, UserRead, LoginRes, LoginPayload, OTPVerifyPayload, RegenerationOtpPayload
from ..middleware.jwt_methods import create_access_token
from ..middleware.verification import send_verification_email, verify_otp, delete_otp_from_redis

router = APIRouter(prefix="/accounts", tags=["accounts"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
admin_ip = os.getenv("ADMIN_IP")

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    exists = await session.scalar(
        select(User).where(
            (User.email == payload.email) | (User.username == payload.username)
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Username or email already registered")

    user_ip = request.client.host
    if user_ip == admin_ip:
        assigned_role = UserRole.ADMIN
    else:
        assigned_role = UserRole.USER
    hashed = pwd_context.hash(payload.password)
    user = User(
        username=payload.username,
        email=payload.email,
        password=hashed,
        role=assigned_role
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    asyncio.create_task(send_verification_email(user.email))
    return user

@router.post("/login", response_model=LoginRes, status_code=status.HTTP_200_OK)
async def login_user(payload: LoginPayload, response: Response, request: Request, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email or password is incorrect")
    if not user.email_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verify your email first")
    if not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email or password is incorrect")
    access_token = create_access_token({"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    )
    print("access_token=> ", request.cookies.get("access_token"))
    return LoginRes(message="Logged in successfully", token=access_token)

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_user_otp(payload: OTPVerifyPayload, session: AsyncSession = Depends(get_db)):
    is_valid = await verify_otp(payload.email, payload.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    asyncio.create_task(delete_otp_from_redis(payload.email))
    return {"message": "Email verified successfully"}

@router.post("/regenerate-otp", status_code=status.HTTP_200_OK)
async def regenerate_otp_for_verify_email(payload: RegenerationOtpPayload,session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    success = asyncio.create_task(send_verification_email(user.email))
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    return {"message": "OTP has been regenerated and sent successfully."}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return {"message": "Logout successfully"}