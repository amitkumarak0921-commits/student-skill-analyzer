"""Optional manual seeding:  python seed_questions.py
The API also does this automatically on startup."""
from app.database.connection import Base, engine
from app.seed_data import SUBJECTS, seed_questions
from app.main import seed_subjects

Base.metadata.create_all(bind=engine)
seed_subjects()
print(f"{seed_questions()} new questions inserted.")
