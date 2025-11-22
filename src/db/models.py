from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from ..accounts.user_roles import UserRole
from sqlalchemy import Enum as SqlEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER)