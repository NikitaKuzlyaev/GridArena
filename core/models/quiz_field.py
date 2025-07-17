import datetime
from typing import List

from sqlalchemy import DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class QuizField(Base):
    __tablename__ = "quiz_field"

    contest: Mapped["Contest"] = relationship(
        back_populates="quiz_field"
    )

    problem_cards: Mapped[List["ProblemCard"]] = relationship(
        back_populates="quiz_field",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    contest_id: Mapped[int] = mapped_column(
        ForeignKey("contest.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    number_of_rows: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("number_of_rows BETWEEN 1 AND 8"),
        nullable=False
    )

    number_of_columns: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("number_of_columns BETWEEN 1 AND 8"),
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
