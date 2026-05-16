# Database Setup

## Option 1: Docker (Recommended when Docker is running)

If you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed **and the Docker daemon is running**:

```powershell
cd "C:\College\proj\major proj"
docker compose up -d
```

This starts PostgreSQL on `localhost:5432` with:
- **User:** postgres  
- **Password:** postgres  
- **Database:** diet_recommendation_db  

The `backend/.env` is pre-configured for this setup.

**If you see** `FileNotFoundError` / `No such file or directory` or "Error while fetching server API version": the Docker (or Podman) daemon is not running or not reachable. Use **Option 2** (install PostgreSQL locally) instead.

---

## Option 2: Install PostgreSQL Manually (use this if Docker isn't working)

### On Windows

1. **Download** PostgreSQL 14+ from https://www.postgresql.org/download/windows/

2. **Install** – during setup, note the password you set for the `postgres` user.

3. **Create the database** (PowerShell or pgAdmin):
   ```sql
   CREATE DATABASE diet_recommendation_db;
   ```

4. **Update `backend/.env`** with your credentials:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/diet_recommendation_db
   ```

### On Linux / WSL (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE diet_recommendation_db;"
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

Then in `backend/.env` use:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/diet_recommendation_db
```

---

## Option 3: Winget (Windows Package Manager)

```powershell
winget install PostgreSQL.PostgreSQL
```

After installation, create the database and update `.env` as in Option 2.

---

## Verify & Run Backend (use the project venv)

Install dependencies and run migrations **inside the backend virtual environment**. Always **cd into backend/** and **activate the venv** before `pip` or `uvicorn` (otherwise: `externally-managed-environment` or `ModuleNotFoundError: No module named 'app'`).

### WSL / Linux

**One-time setup (from project root):**

```bash
cd "/mnt/c/College/proj/major proj/backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

**Every time you run the API** (must be from `backend/` with venv active):

```bash
cd "/mnt/c/College/proj/major proj/backend"
source venv/bin/activate
uvicorn app.main:app --reload
```

If you need to install a new dependency (e.g. after pulling changes): `pip install -r requirements.txt` (with venv active and from `backend/`).

### Windows (PowerShell)

From project root, one-time: `cd backend`, then `python -m venv venv`, `.\venv\Scripts\Activate.ps1`, `pip install -r requirements.txt`, `alembic upgrade head`. To run the API: `cd backend`, `.\venv\Scripts\Activate.ps1`, `uvicorn app.main:app --reload`.
