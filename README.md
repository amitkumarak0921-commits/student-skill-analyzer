# CodeCompass — Student Skill Gap Analyzer

React + Vite + Tailwind frontend, FastAPI backend, MySQL via SQLAlchemy, JWT auth.

Students take three-level assessments (Beginner / Intermediate / Advanced, 10 questions each, 70% to pass)
in **C Programming, Java and DBMS**, then see a topic-by-topic breakdown and what to study next.
Admins can read all submitted feedback.

## Requirements
Python 3.10+, Node.js 20+, MySQL 8+.

## 1. Database
```sql
CREATE DATABASE student_skill_analyzer CHARACTER SET utf8mb4;
```
Tables, subjects, topics and all questions are created and seeded automatically when the backend starts.
(`backend/database/schema.sql` documents the schema.)

## 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env  -> then edit it
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000 — docs: http://127.0.0.1:8000/docs

`.env` settings:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | MySQL connection string. URL-encode special characters in the password (`@` → `%40`). |
| `JWT_SECRET` | Long random string: `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `FRONTEND_URL` | Allowed CORS origin (default `http://localhost:5173`). |
| `ADMIN_EMAILS` | Comma-separated emails that become **ADMIN** when they register or log in. |

## 3. Frontend
```bash
cd frontend
npm install
npm run dev
```
App: http://localhost:5173. To point at a different API, copy `.env.example` to `.env` and set `VITE_API_URL`.

Run both together from the project root (after `npm install` there and the backend venv activated): `npm run dev`.

## Hosting
See **DEPLOY.md** for a free setup (Vercel + Render + Aiven MySQL).

## Upgrading from the earlier version
The schema changed (`assessment_attempts` gained `session_id`, `level` is now an integer, `assessment_results` was removed,
roles are `STUDENT` / `ADMIN`). For a clean start:
```sql
DROP DATABASE student_skill_analyzer; CREATE DATABASE student_skill_analyzer CHARACTER SET utf8mb4;
```

## How assessments work
1. `GET /api/questions/subject/{id}?level=N` (login required) checks that the previous level is passed, picks 10 random
   questions, and returns them with a signed, 2-hour `session_token` that records exactly which questions were issued.
2. `POST /api/questions/submit` grades against that token only, so students cannot choose their own questions or submit
   the same session twice. Progress is stored in the database (`GET /api/questions/progress`) and survives refresh/re-login.

## Question bank
94 questions are included (10+ per subject per level). With exactly ~10 per level, the "random" selection is nearly
the same each time. Add more rows to `backend/app/seed_data.py` (restart the API; only new questions are inserted)
to get real variety — 20–30 per level per subject is a good target.

## Layout
```
backend/app/   main.py, config.py, deps.py (auth/admin), routers/, models/, schemas/, seed_data.py
frontend/src/  App.jsx (routes), context/AuthContext.jsx, pages/, components/, services/api.js
```
