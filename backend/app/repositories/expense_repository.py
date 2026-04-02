from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models import Expense, ExpenseStatus, ExpenseCategory, User
from app.schemas import ExpenseCreate, ExpenseUpdate


class ExpenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, expense_id: str) -> Optional[Expense]:
        result = await self.db.execute(
            select(Expense)
            .options(selectinload(Expense.user))
            .where(Expense.id == expense_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: str, expense_data: ExpenseCreate) -> Expense:
        expense = Expense(
            user_id=user_id,
            title=expense_data.title,
            description=expense_data.description,
            amount=expense_data.amount,
            category=expense_data.category,
            receipt_url=expense_data.receipt_url,
        )
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def update(self, expense: Expense, expense_data: ExpenseUpdate) -> Expense:
        update_data = expense_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(expense, field, value)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def delete(self, expense: Expense) -> None:
        await self.db.delete(expense)
        await self.db.commit()

    async def get_user_expenses(
        self, user_id: str, skip: int = 0, limit: int = 20
    ) -> List[Expense]:
        result = await self.db.execute(
            select(Expense)
            .where(Expense.user_id == user_id)
            .order_by(Expense.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_pending_expenses(
        self, skip: int = 0, limit: int = 20
    ) -> List[Expense]:
        result = await self.db.execute(
            select(Expense)
            .options(selectinload(Expense.user))
            .where(Expense.status == ExpenseStatus.PENDING)
            .order_by(Expense.submitted_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_approved_expenses(
        self, skip: int = 0, limit: int = 20
    ) -> List[Expense]:
        result = await self.db.execute(
            select(Expense)
            .options(selectinload(Expense.user))
            .where(Expense.status == ExpenseStatus.APPROVED)
            .order_by(Expense.submitted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all_expenses(
        self, skip: int = 0, limit: int = 20, status: Optional[ExpenseStatus] = None
    ) -> List[Expense]:
        query = select(Expense).options(selectinload(Expense.user))
        if status:
            query = query.where(Expense.status == status)
        query = query.order_by(Expense.submitted_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def approve(self, expense: Expense, reviewer_id: str) -> Expense:
        expense.status = ExpenseStatus.APPROVED
        expense.reviewed_by = reviewer_id
        expense.reviewed_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def reject(
        self, expense: Expense, reviewer_id: str, reason: str
    ) -> Expense:
        expense.status = ExpenseStatus.REJECTED
        expense.reviewed_by = reviewer_id
        expense.reviewed_at = datetime.utcnow()
        expense.rejection_reason = reason
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def reimburse(self, expense: Expense) -> Expense:
        expense.status = ExpenseStatus.REIMBURSED
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def count_by_status(self) -> dict:
        result = await self.db.execute(
            select(Expense.status, func.count(Expense.id)).group_by(Expense.status)
        )
        return {row[0]: row[1] for row in result.all()}

    async def sum_by_category(self) -> List[dict]:
        result = await self.db.execute(
            select(Expense.category, func.sum(Expense.amount), func.count(Expense.id))
            .group_by(Expense.category)
        )
        return [
            {"category": row[0], "total": float(row[1]), "count": row[2]}
            for row in result.all()
        ]

    async def sum_by_department(self) -> List[dict]:
        result = await self.db.execute(
            select(User.department, func.sum(Expense.amount), func.count(Expense.id))
            .join(User, Expense.user_id == User.id)
            .where(User.department.isnot(None))
            .group_by(User.department)
        )
        return [
            {"department": row[0], "total": float(row[1]), "count": row[2]}
            for row in result.all()
        ]