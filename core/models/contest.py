import datetime
from typing import List

from sqlalchemy import String, DateTime, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class Contest(Base):
    __tablename__ = "contest"

    __table_args__ = (
        CheckConstraint("start_points BETWEEN 0 AND 10000", name="check_start_points"),
        CheckConstraint("number_of_slots_for_problems BETWEEN 1 AND 5", name="check_number_of_slots"),
    )

    quiz_fields: Mapped[List["QuizField"]] = relationship(
        back_populates="contest",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(length=256),
        unique=False,
        nullable=False
    )

    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )

    closed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    start_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    number_of_slots_for_problems: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
