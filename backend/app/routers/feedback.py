from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.deps import get_current_user, require_admin
from app.models import Feedback, User
from app.utils import iso_utc

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

CATEGORIES = {"General", "Assessment", "Questions", "UI/Experience", "Technical Issue"}


class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    category: str = Field(..., max_length=50)
    message: str = Field(..., max_length=2000)


def _row(f: Feedback, with_user: bool = False) -> dict:
    data = {
        "id": f.id,
        "rating": f.rating,
        "category": f.category,
        "message": f.message,
        "created_at": iso_utc(f.created_at),
    }
    if with_user:
        data["user_name"] = f.user.name if f.user else None
        data["user_email"] = f.user.email if f.user else None
    return data


@router.post("/my", status_code=201)
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    message = request.message.strip()
    category = request.category.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Feedback message cannot be empty.")
    if category not in CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid feedback category.")

    feedback = Feedback(user_id=user.id, rating=request.rating, category=category, message=message)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback submitted successfully.", **_row(feedback)}


@router.get("/my")
def get_my_feedback(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = (
        db.query(Feedback)
        .filter(Feedback.user_id == user.id)
        .order_by(Feedback.created_at.desc(), Feedback.id.desc())
        .all()
    )
    return [_row(f) for f in rows]


@router.get("")
def get_all_feedback(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    rows = (
        db.query(Feedback)
        .options(joinedload(Feedback.user))
        .order_by(Feedback.created_at.desc(), Feedback.id.desc())
        .all()
    )
    return {"total": len(rows), "feedback": [_row(f, with_user=True) for f in rows]}
