import random
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import JWT_SECRET
from app.database.connection import get_db
from app.deps import ALGORITHM, get_current_user
from app.models import AssessmentAttempt, Question, Subject, Topic, User, UserAnswer

router = APIRouter(prefix="/api/questions", tags=["Questions"])

QUESTIONS_PER_LEVEL = 10
PASS_PERCENTAGE = 70
DIFFICULTY = {1: "Easy", 2: "Medium", 3: "Hard"}
LEVEL_NAME = {1: "Beginner", 2: "Intermediate", 3: "Advanced"}
SESSION_HOURS = 2


def _highest_passed(db: Session, user_id: int, subject_id: int) -> int:
    value = (
        db.query(func.max(AssessmentAttempt.level))
        .filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.subject_id == subject_id,
            AssessmentAttempt.passed.is_(True),
        )
        .scalar()
    )
    return int(value or 0)


def _require_unlocked(db: Session, user_id: int, subject_id: int, level: int):
    if level > 1 and _highest_passed(db, user_id, subject_id) < level - 1:
        raise HTTPException(
            status_code=403,
            detail=f"You must pass Level {level - 1} before attempting Level {level}.",
        )


# ---------------------------------------------------------
# PROGRESS  (highest passed level per subject)
# ---------------------------------------------------------
@router.get("/progress")
def get_progress(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = (
        db.query(AssessmentAttempt.subject_id, func.max(AssessmentAttempt.level))
        .filter(AssessmentAttempt.user_id == user.id, AssessmentAttempt.passed.is_(True))
        .group_by(AssessmentAttempt.subject_id)
        .all()
    )
    return {"highest_passed": {str(subject_id): int(level) for subject_id, level in rows}}


# ---------------------------------------------------------
# START ASSESSMENT -> 10 random questions + signed session
# ---------------------------------------------------------
@router.get("/subject/{subject_id}")
def start_assessment(
    subject_id: int,
    level: int = Query(..., ge=1, le=3),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not db.get(Subject, subject_id):
        raise HTTPException(status_code=404, detail="Subject not found")

    _require_unlocked(db, user.id, subject_id, level)

    difficulty = DIFFICULTY[level]
    pool = [
        row[0]
        for row in db.query(Question.id)
        .join(Topic, Question.topic_id == Topic.id)
        .filter(Topic.subject_id == subject_id, Question.difficulty == difficulty)
        .all()
    ]
    if len(pool) < QUESTIONS_PER_LEVEL:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Only {len(pool)} {difficulty} questions are available. "
                f"{QUESTIONS_PER_LEVEL} are required."
            ),
        )

    chosen_ids = random.sample(pool, QUESTIONS_PER_LEVEL)
    questions = db.query(Question).filter(Question.id.in_(chosen_ids)).all()
    random.shuffle(questions)

    session_token = jwt.encode(
        {
            "typ": "assessment",
            "sub": str(user.id),
            "sid": uuid.uuid4().hex,
            "subject_id": subject_id,
            "level": level,
            "qids": [q.id for q in questions],
            "exp": datetime.now(timezone.utc) + timedelta(hours=SESSION_HOURS),
        },
        JWT_SECRET,
        algorithm=ALGORITHM,
    )

    return {
        "session_token": session_token,
        "level": level,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty,
                "topic_id": q.topic_id,
            }
            for q in questions
        ],
    }


# ---------------------------------------------------------
# SUBMIT
# ---------------------------------------------------------
class SubmitRequest(BaseModel):
    session_token: str
    answers: dict[str, str]


@router.post("/submit")
def submit_assessment(
    request: SubmitRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        session = jwt.decode(request.session_token, JWT_SECRET, algorithms=[ALGORITHM])
        if session.get("typ") != "assessment" or int(session["sub"]) != user.id:
            raise ValueError("bad session")
        session_id = session["sid"]
        subject_id = int(session["subject_id"])
        level = int(session["level"])
        question_ids = [int(q) for q in session["qids"]]
    except (JWTError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="This assessment session is invalid or has expired. Please start again.",
        )

    if level not in DIFFICULTY:
        raise HTTPException(status_code=400, detail="Invalid level")

    if db.query(AssessmentAttempt.id).filter(AssessmentAttempt.session_id == session_id).first():
        raise HTTPException(status_code=409, detail="This assessment was already submitted.")

    _require_unlocked(db, user.id, subject_id, level)

    answers = {k: v.strip().upper() for k, v in request.answers.items()}
    if any(v not in ("A", "B", "C", "D") for v in answers.values()):
        raise HTTPException(status_code=400, detail="Answers must be A, B, C or D.")

    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    if len(questions) != len(question_ids):
        raise HTTPException(status_code=400, detail="Some questions no longer exist. Please start again.")

    topic_scores: dict[int, dict[str, int]] = {}
    graded = []
    correct = 0
    for q in questions:
        selected = answers.get(str(q.id), "")
        is_correct = selected == q.correct_answer
        correct += int(is_correct)
        bucket = topic_scores.setdefault(q.topic_id, {"correct": 0, "total": 0})
        bucket["total"] += 1
        bucket["correct"] += int(is_correct)
        graded.append((q.id, selected, is_correct))

    total = len(questions)
    percentage = round(correct / total * 100, 2)
    passed = percentage >= PASS_PERCENTAGE

    attempt = AssessmentAttempt(
        user_id=user.id,
        subject_id=subject_id,
        level=level,
        session_id=session_id,
        total_questions=total,
        correct_answers=correct,
        percentage=percentage,
        passed=passed,
    )
    db.add(attempt)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="This assessment was already submitted.")

    db.add_all(
        UserAnswer(
            attempt_id=attempt.id,
            question_id=qid,
            selected_answer=selected,
            is_correct=ok,
        )
        for qid, selected, ok in graded
    )
    db.commit()

    topic_names = dict(
        db.query(Topic.id, Topic.name).filter(Topic.id.in_(list(topic_scores))).all()
    )
    topic_results = sorted(
        (
            {
                "topic": topic_names.get(tid, f"Topic {tid}"),
                "correct": s["correct"],
                "total": s["total"],
                "percentage": round(s["correct"] / s["total"] * 100, 2),
            }
            for tid, s in topic_scores.items()
        ),
        key=lambda t: t["topic"],
    )

    return {
        "subject_id": subject_id,
        "level": level,
        "level_name": LEVEL_NAME[level],
        "correct": correct,
        "total": total,
        "percentage": percentage,
        "passed": passed,
        "next_level": level + 1 if passed and level < 3 else None,
        "topic_results": topic_results,
    }
