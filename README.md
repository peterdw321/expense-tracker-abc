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

## Production URLs

- **Frontend**: https://frontend-kappa-vert-23.vercel.app
- **Backend**: https://expense-tracker-production-0757.up.railway.app
- **API Docs**: https://expense-tracker-production-0757.up.railway.app/docs

## Quick Start

### Backend (Local Development)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set up .env (copy from .env.example)
# Run server
uvicorn app.main:app --reload
```

### Frontend (Local Development)

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

## Project Structure

```
backend/
├── app/
│   ├── api/v1/routes/      # API endpoints
│   ├── core/               # Config, DB, security
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   └── services/           # Business logic
├── alembic/                # Database migrations
├── Dockerfile              # Railway deployment
├── railway.json            # Railway config
└── requirements.txt        # Python dependencies

frontend/
├── src/
│   ├── components/         # React components
│   ├── pages/              # Page components
│   ├── services/           # API calls
│   └── store/              # State management
├── package.json
└── vite.config.ts
```

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repo to Vercel
2. Add environment variable: `VITE_API_BASE_URL=https://expense-tracker-production-0757.up.railway.app/api/v1`
3. Deploy automatically on push to main

### Backend (Railway)

1. Connect your GitHub repo to Railway
2. Add PostgreSQL plugin
3. Set `DATABASE_URL` environment variable (auto-set by Railway)
4. Deploy automatically on push to main

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key
```

### Frontend

```
VITE_API_BASE_URL=http://localhost:8000/api/v1  (local)
VITE_API_BASE_URL=https://expense-tracker-production-0757.up.railway.app/api/v1  (production)
```