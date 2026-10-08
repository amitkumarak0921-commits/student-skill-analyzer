from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database.connection import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectResponse

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])

@router.get("", response_model=list[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return (
        db.query(Subject)
        .options(joinedload(Subject.topics))
        .order_by(Subject.id)
        .all()
    )
