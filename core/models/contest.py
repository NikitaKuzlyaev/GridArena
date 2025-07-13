import datetime

from sqlalchemy import String, DateTime, Integer, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class Contest(Base):
    __tablename__ = "contest"

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
        CheckConstraint("start_points BETWEEN 0 AND 10000"),
        nullable=False,
    )

    number_of_slots_for_problems: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("number_of_slots_for_problems BETWEEN 1 AND 5"),
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
