import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class QuizField(Base):
    __tablename__ = "quiz_field"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    contest_id: Mapped[int] = mapped_column(
        ForeignKey("contest.id"),
        nullable=False
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
