import datetime

from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.database.connection import Base


class SelectedProblem(Base):
    __tablename__ = "selected_problem"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    problem_card_id: Mapped[int] = mapped_column(
        ForeignKey("problem_card.id"),
        nullable=False
    )

    reward_rule: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
