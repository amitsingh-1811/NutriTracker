import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Async connection URL
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# Async SQLAlchemy engine
engine = create_async_engine(DB_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()

# Async helper for getting DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
