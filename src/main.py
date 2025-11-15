from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.database import engine, Base
from src.db.models import User
from src.accounts.routes import router as accounts_router

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.include_router(accounts_router)
    yield

app = FastAPI(title="NutriTracker", lifespan=lifespan)

@app.get("/",status_code=201)
async def get():
    return "inside home"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
