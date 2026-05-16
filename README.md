# Diet LLM Recommendation System

An intelligent diet recommendation system using LLMs for personalized nutrition guidance via text and image-based food logging.

## How it was built

The app was developed incrementally: PostgreSQL + Alembic schema, FastAPI backend (auth, meals, LLM parsing, recommendations), then a Vite/React SPA. See **[BUILD_GUIDE.md](BUILD_GUIDE.md)** for step-by-step replication and **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)** for how each folder and file fits together (including phased creation and per-file roles).

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API routes (auth, users, meals, recommendations)
│   │   ├── core/           # Config, database, security, dependencies
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic (LLM, nutrition, meal, recommendation)
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Seed scripts (foods DB)
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/               # React (Vite) + TypeScript SPA
├── database/               # DB setup docs (Docker vs local Postgres)
├── docs/                   # Report figures/tables index, etc.
├── docker-compose.yml      # Local PostgreSQL
├── BUILD_GUIDE.md
└── PROJECT_STRUCTURE.txt   # Detailed file roles + creation narrative
```

## Setup

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 14+ (or use a cloud DB)
- OpenAI API key

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Unix: source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables

Copy `.env.example` to `.env` and fill in:

```
DATABASE_URL=postgresql://user:password@localhost:5432/diet_db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```

### 4. Database

```bash
# Run migrations
alembic upgrade head

# Seed sample foods
python scripts/seed_foods.py
```

### 5. Run Backend

```bash
cd backend
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### 6. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:3000 (proxies API to backend)

**First time:** Register an account, set profile/goals in Profile, then log meals and view daily summaries on the Dashboard.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login (returns JWT) |
| GET | `/api/v1/auth/me` | Current user (auth required) |
| GET | `/api/v1/users/me` | Profile |
| PUT | `/api/v1/users/me` | Update profile |
| PUT | `/api/v1/users/me/goals` | Update goals |
| POST | `/api/v1/meals/log` | Log meal from text |
| GET | `/api/v1/meals` | Meal history |
| GET | `/api/v1/recommendations/daily` | Today's summary |
| POST | `/api/v1/recommendations/generate` | Generate daily summary |

## Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for Docker full-stack deploy, cloud PaaS (Render/Railway), and production checklists.

Quick Docker deploy (from repo root, after copying `.env.prod.example` → `.env` and filling secrets):

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

## Build Guide

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed step-by-step instructions.
