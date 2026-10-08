import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/student_skill_analyzer",
)
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
# Optional database TLS (needed by hosted MySQL such as Aiven):
#   DB_SSL_CA      path to a CA certificate file, or
#   DB_SSL_CA_PEM  the certificate text itself (handy on Render, where you can't upload files)
DB_SSL_CA = os.getenv("DB_SSL_CA", "").strip()
DB_SSL_CA_PEM = os.getenv("DB_SSL_CA_PEM", "").replace("\\n", "\n").strip()
ADMIN_EMAILS = {
    e.strip().lower()
    for e in os.getenv("ADMIN_EMAILS", "").split(",")
    if e.strip()
}
# FRONTEND_URL may hold several comma-separated origins (no trailing slash).
_frontend_urls = [u.strip().rstrip("/") for u in FRONTEND_URL.split(",") if u.strip()]
CORS_ORIGINS = sorted({
    *_frontend_urls,
    *(u.replace("localhost", "127.0.0.1") for u in _frontend_urls),
    "http://localhost:5173",
    "http://127.0.0.1:5173",
})
