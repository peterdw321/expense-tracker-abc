from pydantic import BaseModel, EmailStr, Field, field_serializer, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models import UserRole, ExpenseCategory, ExpenseStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole = UserRole.EMPLOYEE
    department: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime

    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer('role')
    def serialize_role(self, value: UserRole) -> str:
        if hasattr(value, 'value'):
            return value.value
        return str(value)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ExpenseBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    amount: float = Field(gt=0)
    category: ExpenseCategory
    receipt_url: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[ExpenseCategory] = None
    receipt_url: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: ExpenseStatus
    submitted_at: datetime
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer('user_id')
    def serialize_user_id(self, value: UUID) -> str:
        return str(value)

    @field_serializer('reviewed_by')
    def serialize_reviewed_by(self, value: Optional[UUID]) -> Optional[str]:
        return str(value) if value else None

    @field_serializer('category')
    def serialize_category(self, value: ExpenseCategory) -> str:
        return value.value

    @field_serializer('status')
    def serialize_status(self, value: ExpenseStatus) -> str:
        return value.value


class ApproveRequest(BaseModel):
    pass


class RejectRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    budget_limit: Optional[float] = None


class DepartmentResponse(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        return str(value)


class ReportSummary(BaseModel):
    total_expenses: float
    pending_count: int
    approved_count: int
    rejected_count: int
    reimbursed_count: int


class ReportByCategory(BaseModel):
    category: ExpenseCategory
    total: float
    count: int

    @field_serializer('category')
    def serialize_category(self, value: ExpenseCategory) -> str:
        return value.value


class ReportByDepartment(BaseModel):
    department: str
    total: float
    count: int