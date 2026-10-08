from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    question_text: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    option_a: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    option_b: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    option_c: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    option_d: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    correct_answer: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False
    )

    topic = relationship("Topic")