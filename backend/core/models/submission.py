import datetime
import enum

from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class SubmissionVerdict(enum.Enum):
    ACCEPTED = "ACCEPTED"
    WRONG = "WRONG"
    REJECTED = "REJECTED"


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    selected_problem_id: Mapped[int] = mapped_column(
        ForeignKey("selected_problem.id"),
        nullable=False
    )

    answer: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False
    )

    verdict: Mapped["SubmissionVerdict"] = mapped_column(
        Enum(SubmissionVerdict),
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
