import datetime
import enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class SelectedProblemStatusType(enum.Enum):
    """
    Статус купленной задачи участником.
    """
    ACTIVE = "ACTIVE"  # Активная задача / в работе. Не было успешных посылок.
    SOLVED = "SOLVED"  # Задача решена. Есть успешная посылка.
    FAILED = "FAILED"  # Задача провалена. Например, превышено число неверных попыток.
    REJECTED = "REJECTED"  # Задача отклонена. Например, заблокирована менеджером. Отправлять посылки нельзя.


class SelectedProblem(Base):
    __tablename__ = "selected_problem"

    __table_args__ = (
        Index("idx_selected_problem_id", "id"),
        Index("idx_selected_problem_problem_card_id", "problem_card_id"),
        Index("idx_selected_problem_contestant_id", "contestant_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    problem_card_id: Mapped[int] = mapped_column(
        ForeignKey("problem_card.id", ondelete="CASCADE"),
        nullable=False,
    )

    contestant_id: Mapped[int] = mapped_column(
        ForeignKey("contestant.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[SelectedProblemStatusType] = mapped_column(
        Enum(SelectedProblemStatusType, default="ACTIVE"),
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
