import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


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

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
