# Employee Expense Tracking System - Specification

## 1. Project Overview

**Project Name:** expense-tracker  
**Company:** ABC Corp  
**Type:** Full-stack Web Application  
**Core Functionality:** Employee expense submission, manager approval workflow, and finance reimbursement tracking system  
**Target Users:** Employees (submit expenses), Managers (approve expenses), Finance Team (reimburse and report)

---

## 2. Technical Architecture

### Stack
- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS
- **Backend:** Python FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL
- **Authentication:** JWT with role-based access control (RBAC)
- **Deployment:** Vercel (frontend) + Railway (backend)

### Database Schema

**Users Table**
- id (UUID, PK)
- email (unique)
- password_hash
- full_name
- role (enum: employee, manager, finance)
- department
- created_at
- updated_at

**Expenses Table**
- id (UUID, PK)
- user_id (FK -> Users)
- title
- description
- amount (decimal)
- category (enum: travel, meals, supplies, equipment, entertainment, other)
- receipt_url (optional)
- status (enum: pending, approved, rejected, reimbursed)
- submitted_at
- reviewed_by (FK -> Users, nullable)
- reviewed_at (nullable)
- rejection_reason (nullable)

**Departments Table**
- id (UUID, PK)
- name (unique)
- budget_limit

---

## 3. UI/UX Specification

### Design System

**Color Palette**
- Primary: #1E3A5F (Deep Navy)
- Secondary: #4A90A4 (Steel Blue)
- Accent: #F5A623 (Amber)
- Success: #2ECC71
- Warning: #F39C12
- Error: #E74C3C
- Background: #F8FAFC
- Surface: #FFFFFF
- Text Primary: #1A1A2E
- Text Secondary: #6B7280

**Typography**
- Font Family: "DM Sans" (headings), "IBM Plex Sans" (body)
- Heading 1: 32px, 700 weight
- Heading 2: 24px, 600 weight
- Heading 3: 18px, 600 weight
- Body: 14px, 400 weight
- Small: 12px, 400 weight

**Spacing**
- Base unit: 4px
- Common spacing: 8px, 12px, 16px, 24px, 32px, 48px

**Border Radius**
- Small: 6px
- Medium: 8px
- Large: 12px
- Full: 9999px

**Shadows**
- Card: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)
- Elevated: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)
- Modal: 0 20px 25px rgba(0,0,0,0.15), 0 10px 10px rgba(0,0,0,0.04)

### Layout Structure

**Responsive Breakpoints**
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

**Page Layout**
- Sidebar: 240px fixed (collapsible on mobile)
- Main content: fluid, max-width 1200px
- Header: 64px fixed

### Pages

**1. Login Page**
- Centered card (400px max-width)
- Logo at top
- Email and password fields
- "Remember me" checkbox
- Submit button
- Link to forgot password (placeholder)

**2. Dashboard (Role-based)**

*Employee Dashboard*
- Welcome message with user name
- Quick stats: Total submitted, Pending, Approved, Reimbursed
- Recent expenses list (last 5)
- "Submit New Expense" prominent button

*Manager Dashboard*
- All pending expenses requiring approval
- Team stats summary
- Filter by status/date

*Finance Dashboard*
- All approved expenses ready for reimbursement
- Reimbursement batch summary
- Export to CSV functionality

**3. Expenses List Page**
- Table view with columns: Date, Title, Category, Amount, Status
- Filter by status, category, date range
- Sort by date, amount
- Pagination (20 per page)
- Row click to view detail

**4. Expense Detail Page**
- Full expense information display
- Receipt image viewer (if uploaded)
- Status timeline (submitted -> approved -> reimbursed)
- Action buttons based on role (approve/reject/reimburse)
- Notes/comments section

**5. New Expense Form**
- Title input
- Amount input (with currency)
- Category dropdown
- Date picker (default today)
- Description textarea
- Receipt upload (drag & drop)
- Submit button

**6. Reports Page (Finance only)**
- Date range selector
- Summary by category
- Summary by department
- Total expenses chart
- Export buttons (CSV)

---

## 4. API Specification

### Authentication Endpoints
- `POST /api/v1/auth/login` - Login with email/password
- `POST /api/v1/auth/register` - Register new user (admin only)
- `GET /api/v1/auth/me` - Get current user info

### User Endpoints
- `GET /api/v1/users` - List all users (manager+)
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user

### Expense Endpoints
- `GET /api/v1/expenses` - List expenses (filtered by role)
- `POST /api/v1/expenses` - Create new expense
- `GET /api/v1/expenses/{id}` - Get expense detail
- `PUT /api/v1/expenses/{id}` - Update expense (if pending)
- `DELETE /api/v1/expenses/{id}` - Delete expense (if pending)
- `POST /api/v1/expenses/{id}/approve` - Approve expense (manager)
- `POST /api/v1/expenses/{id}/reject` - Reject expense (manager)
- `POST /api/v1/expenses/{id}/reimburse` - Mark as reimbursed (finance)

### Report Endpoints
- `GET /api/v1/reports/summary` - Get expense summary by period
- `GET /api/v1/reports/by-category` - Get expenses grouped by category
- `GET /api/v1/reports/by-department` - Get expenses grouped by department

---

## 5. Security Requirements

- Passwords hashed with bcrypt (min 8 chars)
- JWT tokens: 15 min access, 7 day refresh
- Role-based access control on all endpoints
- CORS restricted to frontend origin
- Rate limiting on auth endpoints (10/min)
- Input validation on all endpoints (Pydantic)
- SQL injection prevention (parameterized queries)

---

## 6. Acceptance Criteria

1. User can register/login and receive JWT token
2. Employee can submit expense with receipt upload
3. Employee can view their expense history
4. Manager can view all pending expenses from their team
5. Manager can approve or reject expenses with reason
6. Finance can mark expenses as reimbursed
7. Finance can export expense reports to CSV
8. All forms have proper validation and error messages
9. Responsive design works on mobile/tablet/desktop
10. All API endpoints return appropriate status codes

---

## 7. Environment Variables

### Backend
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- CORS_ORIGINS

### Frontend
- VITE_API_BASE_URL