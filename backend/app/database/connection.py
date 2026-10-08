import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL, DB_SSL_CA, DB_SSL_CA_PEM


def _ssl_connect_args() -> dict:
    """TLS settings for hosted MySQL. Local databases are unaffected unless the env vars are set."""
    if not DATABASE_URL.startswith("mysql"):
        return {}
    ca_path = DB_SSL_CA
    if DB_SSL_CA_PEM:
        handle = tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False)
        handle.write(DB_SSL_CA_PEM + "\n")
        handle.close()
        ca_path = handle.name
    if ca_path:
        if not os.path.exists(ca_path):
            raise RuntimeError(f"DB_SSL_CA file not found: {ca_path}")
        return {"ssl": {"ca": ca_path}}
    return {}


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,  # hosted databases close idle connections
    connect_args=_ssl_connect_args(),
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
