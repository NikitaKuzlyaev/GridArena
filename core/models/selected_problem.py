import datetime
import enum

from sqlalchemy import DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class SelectedProblemStatusType(enum.Enum):
    ACTIVE = "ACTIVE"
    SOLVED = "SOLVED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


class SelectedProblem(Base):
    __tablename__ = "selected_problem"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    problem_card_id: Mapped[int] = mapped_column(
        ForeignKey("problem_card.id"),
        nullable=False
    )

    contestant_id: Mapped[int] = mapped_column(
        ForeignKey("contestant.id"),
        nullable=False
    )

    status: Mapped[SelectedProblemStatusType] = mapped_column(
        Enum(SelectedProblemStatusType)
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
