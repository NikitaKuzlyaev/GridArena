import datetime

from sqlalchemy import String, DateTime, Integer, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class ProblemCard(Base):
    __tablename__ = "problem_card"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.id"),
        nullable=False
    )

    category_name: Mapped[str] = mapped_column(
        String(length=32),
        unique=False,
        nullable=True
    )

    category_price: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("category_price BETWEEN 0 AND 10000"),
        nullable=False,
    )

    quiz_field_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_field.id"),
        nullable=False
    )

    row: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    column: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
