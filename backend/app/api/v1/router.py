from fastapi import APIRouter
from app.api.v1.routes import auth, users, expenses, reports

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(expenses.router)
api_router.include_router(reports.router)