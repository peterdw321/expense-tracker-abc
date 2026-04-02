from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.expense_repository import ExpenseRepository
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.models import Expense, ExpenseStatus


class ExpenseService:
    def __init__(self, db: AsyncSession):
        self.repo = ExpenseRepository(db)

    async def get_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        return await self.repo.get_by_id(expense_id)

    async def create_expense(self, user_id: str, expense_data: ExpenseCreate) -> Expense:
        return await self.repo.create(user_id, expense_data)

    async def update_expense(self, expense: Expense, expense_data: ExpenseUpdate) -> Expense:
        if expense.status != ExpenseStatus.PENDING:
            raise ValueError("Can only update pending expenses")
        return await self.repo.update(expense, expense_data)

    async def delete_expense(self, expense: Expense) -> None:
        if expense.status != ExpenseStatus.PENDING:
            raise ValueError("Can only delete pending expenses")
        await self.repo.delete(expense)

    async def get_user_expenses(self, user_id: str, skip: int = 0, limit: int = 20) -> List[Expense]:
        return await self.repo.get_user_expenses(user_id, skip, limit)

    async def get_pending_expenses(self, skip: int = 0, limit: int = 20) -> List[Expense]:
        return await self.repo.get_pending_expenses(skip, limit)

    async def get_approved_expenses(self, skip: int = 0, limit: int = 20) -> List[Expense]:
        return await self.repo.get_approved_expenses(skip, limit)

    async def get_all_expenses(self, skip: int = 0, limit: int = 20, status: Optional[ExpenseStatus] = None) -> List[Expense]:
        return await self.repo.get_all_expenses(skip, limit, status)

    async def approve_expense(self, expense: Expense, reviewer_id: str) -> Expense:
        if expense.status != ExpenseStatus.PENDING:
            raise ValueError("Can only approve pending expenses")
        return await self.repo.approve(expense, reviewer_id)

    async def reject_expense(self, expense: Expense, reviewer_id: str, reason: str) -> Expense:
        if expense.status != ExpenseStatus.PENDING:
            raise ValueError("Can only reject pending expenses")
        return await self.repo.reject(expense, reviewer_id, reason)

    async def reimburse_expense(self, expense: Expense) -> Expense:
        if expense.status != ExpenseStatus.APPROVED:
            raise ValueError("Can only reimburse approved expenses")
        return await self.repo.reimburse(expense)

    async def get_status_counts(self) -> dict:
        return await self.repo.count_by_status()

    async def get_expenses_by_category(self) -> List[dict]:
        return await self.repo.sum_by_category()

    async def get_expenses_by_department(self) -> List[dict]:
        return await self.repo.sum_by_department()