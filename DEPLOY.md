# Hosting CodeCompass for free

Frontend → **Vercel**, backend → **Render**, database → **Aiven MySQL**. Do the steps in this order.
Free-tier caveat: Render's free web service sleeps after ~15 minutes without traffic, so the first
request after a quiet period is slow (often ~30 s). The login page may look stuck once; wait and retry.

## 0. Before you start
- Do **not** commit `backend/.env` (already in `.gitignore`).
- Generate a **new** `JWT_SECRET` for production:
  `python -c "import secrets; print(secrets.token_urlsafe(48))"`
  (`render.yaml` can also generate one for you.)

## 1. Put the project on GitHub
```powershell
cd path\to\student-skill-analyzer
git init
git add .
git commit -m "Initial commit"
```
Create an empty repository on github.com (no README), then run the two commands GitHub shows
(`git remote add origin ...` and `git push -u origin main`).
Check on GitHub that `.env` and `venv` are NOT in the repository.

## 2. Database — Aiven (free MySQL)
1. Sign up at aiven.io and create a **MySQL** service on the **Free** plan.
2. Wait until it is **Running**, then open its overview page and note: **host, port, user, password, database name**
   (the database is usually `defaultdb`).
3. On the same page download or copy the **CA certificate**.
4. Build your connection string (URL-encode special characters in the password, `@` → `%40`):
   ```
   mysql+pymysql://USER:PASSWORD@HOST:PORT/defaultdb
   ```
The API creates all tables and the question bank on first start; nothing to import.

## 3. Backend — Render
1. render.com → **New → Web Service** → connect your GitHub repo.
   (Or **New → Blueprint**, which reads `render.yaml` from the repo root.)
2. Settings if you fill them in by hand:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance type: **Free**
   - Health Check Path: `/api/health`
3. Environment variables:

   | Key | Value |
   |---|---|
   | `PYTHON_VERSION` | `3.12.8` |
   | `DATABASE_URL` | the connection string from step 2 |
   | `DB_SSL_CA_PEM` | the full CA certificate text (including the BEGIN/END lines) |
   | `JWT_SECRET` | your new long random secret |
   | `ADMIN_EMAILS` | your email |
   | `FRONTEND_URL` | leave for now; set in step 5 |

4. Deploy. When the log shows `Application startup complete`, open
   `https://YOUR-SERVICE.onrender.com/api/health` → `{"status":"ok"}`, and
   `https://YOUR-SERVICE.onrender.com/api/subjects` should list 3 subjects.

## 4. Frontend — Vercel
1. vercel.com → **Add New → Project** → import the same repo.
2. Root Directory: `frontend`. Framework preset: **Vite** (build `npm run build`, output `dist`).
3. Environment variable: `VITE_API_URL` = `https://YOUR-SERVICE.onrender.com` (no trailing slash).
4. Deploy and note your URL, e.g. `https://your-app.vercel.app`.
   `frontend/vercel.json` makes refreshing pages like `/dashboard` work.

## 5. Connect them
In Render → your service → Environment, set `FRONTEND_URL` to your Vercel URL
(no trailing slash; several allowed, comma-separated), then let it redeploy.
Without this the browser blocks requests and you'll see "Cannot reach the server".

## 6. Test
Open the Vercel URL → register with the email in `ADMIN_EMAILS` → check the **All Feedback** link → take a Level 1 test.

## Troubleshooting
| Symptom | Likely cause |
|---|---|
| "Cannot reach the server" | `FRONTEND_URL` on Render doesn't exactly match your Vercel URL; or Render is waking up — wait 30–60 s |
| Render deploy fails on install | set `PYTHON_VERSION` to `3.12.8` |
| `Access denied` / `SSL` errors in Render logs | wrong password in `DATABASE_URL`, or `DB_SSL_CA_PEM` missing/incomplete |
| 404 on refresh at `/dashboard` | `frontend/vercel.json` not deployed — Root Directory must be `frontend` |
| Changed `VITE_API_URL` but nothing changed | Vite bakes it in at build time — redeploy the frontend |
| Admin link missing | log out and in again after setting `ADMIN_EMAILS`; the email must match exactly |
