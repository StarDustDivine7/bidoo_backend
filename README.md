# Bidoo ERP Backend

FastAPI based simple ERP backend jisme:
- Admin aur employee dono same `users` table me store hote hain
- JWT login system hai
- Employee check-in, lunch start, lunch end, check-out kar sakta hai
- Employee daily work update bhej sakta hai
- Admin user create kar sakta hai
- Admin tasks assign kar sakta hai
- Admin user-wise tracking aur dashboard dekh sakta hai

## Folder Structure

```text
app/
  api/
    deps.py              # Auth dependencies
    routes.py            # Saare API endpoints
  core/
    config.py            # .env settings
    database.py          # SQLAlchemy setup
    security.py          # Password hashing + JWT
  model/
    user.py              # User model
    task.py              # Task model
    attendance.py        # Attendance model
    work_log.py          # Work log model
  repository/
    *.py                 # DB access layer
  services/
    *.py                 # Business logic
  schemas/
    *.py                 # Request/response schemas
  main.py                # FastAPI app entrypoint
```

## Main Flow

### Admin
- Login karega `/api/v1/auth/login`
- User create karega `/api/v1/admin/users`
- Task assign karega `/api/v1/admin/tasks`
- Dashboard dekhega `/api/v1/admin/dashboard`
- Kisi bhi employee ka tracking dekhega `/api/v1/admin/users/{user_id}/tracking`

### Employee
- Login karega `/api/v1/auth/login`
- Profile dekhega `/api/v1/users/me`
- Check-in karega `/api/v1/attendance/check-in`
- Lunch start/end mark karega
- Check-out karega
- Daily work update bhejega `/api/v1/work-logs`
- Apne tasks aur updates dekhega

## Local Run

Project root se run karein:

```bash
uvicorn app.main:app --reload --port 8000
```

## Important Note

`app/` folder ke andar jaake `uvicorn app.main:app` mat chalaiye.
Warna Python kisi aur installed `app` package ko import kar sakta hai.

## First Admin Create Karne Ka Tarika

Abhi API me admin-only create route hai, isliye initial admin create karne ke liye aapko ek seed script ya direct DB insert ki zarurat hogi. Quick option:
- temporary DB me ek admin row insert karo
- ya mujhse bolo, main ek `seed_admin.py` bana deta hoon

## Render Deploy

Details ke liye [docs/DEPLOY_RENDER.md](/Users/debabratadutta/StudioProjects/bidoo_backend/docs/DEPLOY_RENDER.md) dekhein.
