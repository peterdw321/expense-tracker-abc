from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.routes.auth import require_role
from app.services.expense_service import ExpenseService
from app.schemas import ReportSummary, ReportByCategory, ReportByDepartment
from app.models import UserRole, ExpenseStatus

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary", response_model=ReportSummary)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(UserRole.MANAGER, UserRole.FINANCE))
):
    service = ExpenseService(db)
    status_counts = await service.get_status_counts()
    expenses = await service.get_all_expenses(skip=0, limit=10000)
    total = sum(float(e.amount) for e in expenses)
    return ReportSummary(
        total_expenses=total,
        pending_count=status_counts.get(ExpenseStatus.PENDING, 0),
        approved_count=status_counts.get(ExpenseStatus.APPROVED, 0),
        rejected_count=status_counts.get(ExpenseStatus.REJECTED, 0),
        reimbursed_count=status_counts.get(ExpenseStatus.REIMBURSED, 0),
    )


@router.get("/by-category", response_model=List[ReportByCategory])
async def get_by_category(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(UserRole.MANAGER, UserRole.FINANCE))
):
    service = ExpenseService(db)
    results = await service.get_expenses_by_category()
    return [ReportByCategory(category=r["category"], total=r["total"], count=r["count"]) for r in results]


@router.get("/by-department", response_model=List[ReportByDepartment])
async def get_by_department(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_role(UserRole.MANAGER, UserRole.FINANCE))
):
    service = ExpenseService(db)
    results = await service.get_expenses_by_department()
    return [ReportByDepartment(department=r["department"], total=r["total"], count=r["count"]) for r in results]