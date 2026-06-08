# Render Deployment Guide

## 1. Required Environment Variables

Render dashboard me ye values add karein:

```env
APP_NAME=Bidoo ERP Backend
APP_VERSION=1.0.0
APP_ENV=production
API_V1_PREFIX=/api/v1
DATABASE_URL=<render-postgres-internal-url>
JWT_SECRET_KEY=<strong-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## 2. Build Command

```bash
pip install -r requirements.txt
```

## 3. Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 4. Recommended Render Setup

- Web Service: Python
- Python Version: 3.11
- Root Directory: project root
- Auto Deploy: optional

## 5. Production Notes

- Development me `Base.metadata.create_all()` chal raha hai.
- Production best practice: Alembic migrations use karein.
- `JWT_SECRET_KEY` strong aur random hona chahiye.
- Postgres Render ka managed database use karein.

## 6. Next Better Step

Production-grade version ke liye ye add karein:
- Alembic migrations
- seed admin command
- refresh token flow
- audit logs
- pagination and filters
