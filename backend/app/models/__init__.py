import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    FINANCE = "finance"


class ExpenseCategory(enum.Enum):
    TRAVEL = "travel"
    MEALS = "meals"
    SUPPLIES = "supplies"
    EQUIPMENT = "equipment"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"


class ExpenseStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REIMBURSED = "reimbursed"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    expenses = relationship("Expense", back_populates="user")
    reviewed_expenses = relationship("Expense", back_populates="reviewer")


class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    budget_limit = Column(Numeric(12, 2), nullable=True)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    receipt_url = Column(String(500), nullable=True)
    status = Column(Enum(ExpenseStatus), default=ExpenseStatus.PENDING, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    user = relationship("User", back_populates="expenses", foreign_keys=[user_id])
    reviewer = relationship("User", back_populates="reviewed_expenses", foreign_keys=[reviewed_by])