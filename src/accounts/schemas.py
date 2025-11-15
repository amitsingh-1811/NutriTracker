from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str | None = None

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class LoginRes(BaseModel):
    message: str
    token: str

class OTPVerifyPayload(BaseModel):
    email: EmailStr
    otp: str

class RegenerationOtpPayload(BaseModel):
    email: EmailStr