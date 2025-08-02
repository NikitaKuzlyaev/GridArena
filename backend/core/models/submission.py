import datetime
import enum

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Enum,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class SubmissionVerdict(enum.Enum):
    """
    Статус посылки (решения) участника по выбранной задаче.
    """

    # Посылка обрабатывается. В нормальном сценарии этот вердикт пропускается или не существует достаточно долго
    PROCESSING = "PROCESSING"
    ACCEPTED = "ACCEPTED"  # Принято. Посылка засчитана как верная.
    WRONG = "WRONG"  # Ответ неверный.
    # Решение отклонено, оно продолжает существовать, но не должно влиять на что-либо (как будто его не было)
    REJECTED = "REJECTED"


class Submission(Base):
    __tablename__ = "submission"

    __table_args__ = (
        Index("idx_submission_id", "id"),
        Index("idx_submission_selected_problem_id", "selected_problem_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    selected_problem_id: Mapped[int] = mapped_column(
        ForeignKey("selected_problem.id", ondelete="CASCADE"),
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
    )

    verdict: Mapped["SubmissionVerdict"] = mapped_column(
        Enum(SubmissionVerdict, default=SubmissionVerdict.PROCESSING),
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
