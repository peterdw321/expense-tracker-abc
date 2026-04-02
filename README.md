# Employee Expense Tracking System

A full-stack employee expense tracking application for ABC Corp with role-based access control (Employee, Manager, Finance).

## Features

- **Employee**: Submit expenses, view history, track reimbursement status
- **Manager**: Approve/reject pending expenses from team
- **Finance**: Mark expenses as reimbursed, generate reports

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Auth**: JWT with role-based access control

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set up .env (copy from .env.example)
# Run server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Demo Accounts

- Employee: `employee@abc.com` / `password123`
- Manager: `manager@abc.com` / `password123`
- Finance: `finance@abc.com` / `password123`

## API Documentation

Once running, visit `http://localhost:8000/docs` for Swagger UI.

## Deployment

- Frontend: Vercel
- Backend: Railway (with PostgreSQL)