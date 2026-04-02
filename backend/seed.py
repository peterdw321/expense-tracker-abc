import asyncio
from uuid import uuid4
from app.core.database import AsyncSessionLocal
from app.models import User, UserRole, Expense, ExpenseCategory, ExpenseStatus
from app.core.security import get_password_hash
from datetime import datetime, timedelta


async def seed_data():
    async with AsyncSessionLocal() as db:
        employee = User(
            id=uuid4(),
            email="employee@abc.com",
            password_hash=get_password_hash("password123"),
            full_name="John Employee",
            role=UserRole.EMPLOYEE,
            department="Engineering",
        )
        db.add(employee)

        manager = User(
            id=uuid4(),
            email="manager@abc.com",
            password_hash=get_password_hash("password123"),
            full_name="Jane Manager",
            role=UserRole.MANAGER,
            department="Engineering",
        )
        db.add(manager)

        finance = User(
            id=uuid4(),
            email="finance@abc.com",
            password_hash=get_password_hash("password123"),
            full_name="Bob Finance",
            role=UserRole.FINANCE,
            department="Finance",
        )
        db.add(finance)

        await db.commit()
        print("Users seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_data())