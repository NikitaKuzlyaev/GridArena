import datetime
import uuid

from sqlalchemy import String, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from backend.core.database.connection import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("domain_number", "username", name="uq_user_domain_username"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    domain_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(64),
        unique=False,
        nullable=False
    )

    uuid: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now()
    )
