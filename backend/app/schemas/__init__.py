from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
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
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


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
    id: str
    user_id: str
    status: ExpenseStatus
    submitted_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

    class Config:
        from_attributes = True


class ApproveRequest(BaseModel):
    pass


class RejectRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    budget_limit: Optional[float] = None


class DepartmentResponse(DepartmentBase):
    id: str

    class Config:
        from_attributes = True


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


class ReportByDepartment(BaseModel):
    department: str
    total: float
    count: int