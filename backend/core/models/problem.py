import datetime
from typing import List

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class Problem(Base):
    __tablename__ = "problem"

    problem_cards: Mapped[List["ProblemCard"]] = relationship(
        back_populates="problem"
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    statement: Mapped[str] = mapped_column(
        String(length=2048),
        nullable=True
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
