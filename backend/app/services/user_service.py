from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.models import User
from app.core.security import verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.repo.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repo.get_by_email(email)

    async def create_user(self, user_data: UserCreate) -> User:
        existing = await self.repo.get_by_email(user_data.email)
        if existing:
            raise ValueError("Email already registered")
        return await self.repo.create(user_data)

    async def update_user(self, user: User, user_data: UserUpdate) -> User:
        return await self.repo.update(user, user_data)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.get_all(skip, limit)