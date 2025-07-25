import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class ProblemCard(Base):
    __tablename__ = "problem_card"

    __table_args__ = (
        CheckConstraint("category_price BETWEEN 0 AND 10000", name="check_category_price"),
    )

    problem: Mapped[Optional["Problem"]] = relationship(
        back_populates="problem_cards",
        passive_deletes=True,
        uselist=False
    )

    quiz_field: Mapped["QuizField"] = relationship(
        back_populates="problem_cards"
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.id", ondelete="SET NULL"),
        nullable=True
    )

    category_name: Mapped[str] = mapped_column(
        String(length=32),
        unique=False,
        nullable=True
    )

    category_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quiz_field_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_field.id", ondelete="CASCADE"),
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
