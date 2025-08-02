import datetime
import enum

from sqlalchemy import (
    String,
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class ContestantLogLevelType(enum.Enum):
    """
    Уровень лога. Обозначает тип лога, его серьезность/критичность или его цель.

    Например, INFO - лог, в котором содержится информационное сообщение, в нейтральном контексте.
    """
    INFO = "INFO"  # Информационное сообщение.
    DEBUG = "DEBUG"  # Отладочное сообщение. Не должно появляться у участников в нормальном сценарии.
    ATTENTION = "ATTENTION"  # Предупреждающее сообщение.
    ERROR = "ERROR"  # Сообщение об ошибке. Не должно появляться у участников в нормальном сценарии.


class ContestantLog(Base):
    __tablename__ = "contestant_log"

    __table_args__ = (
        Index("idx_contestant_log_id", "id"),
        Index("idx_contestant_log_contestant_id", "contestant_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    contestant_id: Mapped[int] = mapped_column(
        ForeignKey("contestant.id", ondelete="CASCADE"),
        nullable=False,
    )

    level_type: Mapped["ContestantLogLevelType"] = mapped_column(
        Enum(ContestantLogLevelType),
        default=ContestantLogLevelType.INFO,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        String(length=512),
        unique=False,
        nullable=True,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
