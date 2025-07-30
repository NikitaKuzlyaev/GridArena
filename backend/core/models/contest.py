import datetime
import enum

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    CheckConstraint,
    Enum,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class ContestRuleType(enum.Enum):
    DEFAULT = "DEFAULT"
    BURNING_ALL = "BURNING_ALL"
    BURNING_SELECTED = "BURNING_SELECTED"


class Contest(Base):
    __tablename__ = "contest"

    __table_args__ = (
        CheckConstraint("start_points BETWEEN 0 AND 10000", name="check_start_points"),
        CheckConstraint("number_of_slots_for_problems BETWEEN 1 AND 5", name="check_number_of_slots"),
    )

    quiz_field: Mapped["QuizField"] = relationship(
        back_populates="contest",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
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

    rule_type: Mapped["ContestRuleType"] = mapped_column(
        Enum(ContestRuleType),
        default=ContestRuleType.DEFAULT,
    )

    flag_user_can_have_negative_points: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
