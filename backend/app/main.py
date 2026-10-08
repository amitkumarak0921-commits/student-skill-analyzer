from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.database.connection import Base, SessionLocal, engine
from app.models import Subject, Topic
from app.routers import auth, feedback, questions, subjects
from app.seed_data import SUBJECTS, seed_questions


def seed_subjects():
    db = SessionLocal()
    try:
        if db.query(Subject).count() > 0:
            return
        for name, (description, topics) in SUBJECTS.items():
            subject = Subject(name=name, description=description)
            subject.topics = [Topic(name=t) for t in topics]
            db.add(subject)
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_subjects()
    seed_questions()  # only inserts questions that are not already present
    yield


app = FastAPI(title="CodeCompass API", version="1.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(questions.router)
app.include_router(feedback.router)


@app.get("/")
def root():
    return {"message": "CodeCompass API is running"}


@app.get("/api/health")
def health():
    return {"status": "ok"}
