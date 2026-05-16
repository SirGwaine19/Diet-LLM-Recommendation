# Deployment Guide

This project is a **FastAPI backend**, **React (Vite) frontend**, and **PostgreSQL** database. Choose one path below.

---

## Option A: Docker (recommended for demo / VPS / viva)

Runs Postgres, API, and web UI together. The frontend nginx container proxies `/api` to the backend.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine on Linux
- OpenAI API key

### Steps

1. **Create production env file** at the repository root:

   ```powershell
   cd "C:\College\proj\major proj"
   copy .env.prod.example .env
   ```

   Edit `.env` and set at minimum:

   - `SECRET_KEY` — run `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `OPENAI_API_KEY`
   - `POSTGRES_PASSWORD` (strong password)
   - `CORS_ORIGINS` — include your public URL, e.g. `http://YOUR_SERVER_IP` or `https://yourdomain.com`

2. **Build and start**:

   ```powershell
   docker compose -f docker-compose.prod.yml up -d --build
   ```

3. **Open the app**: http://localhost (or http://YOUR_SERVER_IP if on a VPS)

4. **Check health**:

   - App UI: port `80` (or `APP_PORT` from `.env`)
   - API health: http://localhost/health
   - Swagger (proxied): http://localhost/docs

5. **First-time data**: `SEED_FOODS=true` in `.env` seeds the food table on first backend start. Set to `false` after that to speed restarts.

### Useful commands

```powershell
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build   # after code changes
```

### VPS (DigitalOcean, AWS EC2, Azure VM, etc.)

1. Install Docker on the server.
2. Clone the repo, create `.env` as above.
3. Open firewall port **80** (and **443** if you add HTTPS).
4. Run `docker compose -f docker-compose.prod.yml up -d --build`.
5. Point your domain A-record to the server IP; add the domain to `CORS_ORIGINS`.

For HTTPS, put **Caddy** or **nginx** in front with Let’s Encrypt, or use a cloud load balancer with TLS.

---

## Option B: Split hosting (Render / Railway / Fly)

Host the database and API on a PaaS, and the frontend as static files.

### 1. PostgreSQL

Create a managed Postgres instance (Render PostgreSQL, Neon, Supabase, Railway). Copy the connection URL.

### 2. Backend (example: Render Web Service)

| Setting | Value |
|--------|--------|
| Root directory | `backend` |
| Build command | `pip install -r requirements.txt && alembic upgrade head` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

**Environment variables:**

| Variable | Notes |
|----------|--------|
| `DATABASE_URL` | From your Postgres provider (`postgres://` is auto-fixed to `postgresql://`) |
| `SECRET_KEY` | Long random string |
| `OPENAI_API_KEY` | Your OpenAI key |
| `DEBUG` | `false` |
| `CORS_ORIGINS` | Your frontend URL, e.g. `https://your-app.onrender.com` |

After deploy, run seed once (Render shell or locally against prod DB):

```bash
python scripts/seed_foods.py
```

Note the public API URL, e.g. `https://diet-api.onrender.com`.

### 3. Frontend (example: Render Static Site)

| Setting | Value |
|--------|--------|
| Root directory | `frontend` |
| Build command | `npm install && npm run build` |
| Publish directory | `dist` |

**Build environment variable:**

```
VITE_API_URL=https://YOUR-BACKEND-HOST/api/v1
```

Redeploy the frontend whenever the backend URL changes.

---

## Option C: Local production build (no Docker)

**Backend** (with Postgres already running via `docker compose up -d` or local install):

```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python scripts\seed_foods.py
$env:DEBUG="false"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**

```powershell
cd frontend
npm install
npm run build
npm run preview
```

For a real deployment, serve `frontend/dist` with nginx and proxy `/api` to port 8000 (same pattern as `frontend/nginx.conf`).

---

## Checklist before going live

- [ ] `SECRET_KEY` is unique and not committed to git
- [ ] `DEBUG=false` in production
- [ ] `CORS_ORIGINS` includes only your real frontend URL(s)
- [ ] Database migrations applied (`alembic upgrade head`)
- [ ] Food seed run at least once
- [ ] OpenAI billing/limits configured
- [ ] Firewall exposes only needed ports (80/443)

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| CORS errors in browser | Add your frontend origin to `CORS_ORIGINS` (comma-separated, no trailing slash on path) |
| `relation does not exist` | Run `alembic upgrade head` on the backend |
| Empty meal matching | Run `python scripts/seed_foods.py` |
| Frontend can’t reach API (split deploy) | Set `VITE_API_URL` at **build** time to `https://backend-host/api/v1` |
| Render DB URL uses `postgres://` | Handled automatically in `app/core/config.py` |

For local development, see [README.md](README.md) and [database/SETUP.md](database/SETUP.md).
