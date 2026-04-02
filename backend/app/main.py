from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import enum
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL: str = os.environ.get('DATABASE_URL', '')
if not DATABASE_URL:
    logger.error("DATABASE_URL not set!")
else:
    logger.info(f"DATABASE_URL: {DATABASE_URL[:30]}...")

if not DATABASE_URL.startswith('postgresql+asyncpg://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)

logger.info(f"Final DATABASE_URL: {DATABASE_URL[:50]}...")

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

Base = declarative_base()


class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    FINANCE = "finance"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Lifespan startup complete")
    yield
    
    yield


app = FastAPI(
    title="Expense Tracker",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.router import api_router
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "project": "Expense Tracker"}


@app.post("/debug/seed")
async def debug_seed():
    from uuid import uuid4
    from passlib.context import CryptContext
    from sqlalchemy import text
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pw_hash = pwd_context.hash("password123")
    
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text("""INSERT INTO users (id, email, password_hash, full_name, role, department) 
                       VALUES (:id, :email, :pw_hash, :name, :role, :dept)"""),
                {"id": str(uuid4()), "email": "employee@abc.com", "pw_hash": pw_hash, "name": "John Employee", "role": "EMPLOYEE", "dept": "Engineering"}
            )
            await conn.execute(
                text("""INSERT INTO users (id, email, password_hash, full_name, role, department) 
                       VALUES (:id, :email, :pw_hash, :name, :role, :dept)"""),
                {"id": str(uuid4()), "email": "manager@abc.com", "pw_hash": pw_hash, "name": "Jane Manager", "role": "MANAGER", "dept": "Engineering"}
            )
            await conn.execute(
                text("""INSERT INTO users (id, email, password_hash, full_name, role, department) 
                       VALUES (:id, :email, :pw_hash, :name, :role, :dept)"""),
                {"id": str(uuid4()), "email": "finance@abc.com", "pw_hash": pw_hash, "name": "Bob Finance", "role": "FINANCE", "dept": "Finance"}
            )
            await conn.commit()
        return {"status": "seeded"}
    except Exception as e:
        logger.error(f"Seed error: {e}")
        return {"error": str(e)}


@app.get("/debug/db")
async def debug_db():
    from sqlalchemy import text
    async with engine.begin() as conn:
        # Check role enum values
        result = await conn.execute(text("SELECT enumlabel FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'userrole')"))
        role_values = [r[0] for r in result.fetchall()]
        
        # Check user count
        result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        
        result = await conn.execute(text("SELECT email, role FROM users LIMIT 5"))
        rows = result.fetchall()
        return {"role_values": role_values, "user_count": count, "users": [{"email": r[0], "role": r[1]} for r in rows]}