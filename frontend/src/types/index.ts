export type UserRole = 'employee' | 'manager' | 'finance';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  department?: string;
  created_at: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export type ExpenseCategory = 'travel' | 'meals' | 'supplies' | 'equipment' | 'entertainment' | 'other';

export type ExpenseStatus = 'pending' | 'approved' | 'rejected' | 'reimbursed';

export interface Expense {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  amount: number;
  category: ExpenseCategory;
  receipt_url?: string;
  status: ExpenseStatus;
  submitted_at: string;
  reviewed_by?: string;
  reviewed_at?: string;
  rejection_reason?: string;
}

export interface ExpenseCreate {
  title: string;
  description?: string;
  amount: number;
  category: ExpenseCategory;
  receipt_url?: string;
}

export interface ReportSummary {
  total_expenses: number;
  pending_count: number;
  approved_count: number;
  rejected_count: number;
  reimbursed_count: number;
}

export interface ReportByCategory {
  category: ExpenseCategory;
  total: number;
  count: number;
}

export interface ReportByDepartment {
  department: string;
  total: number;
  count: number;
}