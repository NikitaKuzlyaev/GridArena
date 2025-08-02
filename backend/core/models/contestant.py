import datetime

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class Contestant(Base):
    __tablename__ = "contestant"

    __table_args__ = (
        Index("idx_contestant_id", "id"),
        Index("idx_contestant_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(length=256),
        unique=False,
        nullable=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
