import enum

from sqlalchemy import Enum
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.connection import Base


class PermissionActionType(enum.Enum):
    # --- [CONTEST] ---
    ADMIN = "ADMIN"
    EDIT = "EDIT"


class PermissionResourceType(enum.Enum):
    CONTEST = "CONTEST"


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    resource_type: Mapped[PermissionResourceType] = mapped_column(
        Enum(PermissionResourceType)
    )

    resource_id: Mapped[int] = mapped_column(
        nullable=True
    )

    permission_type: Mapped[PermissionActionType] = mapped_column(
        Enum(PermissionActionType)
    )

    __table_args__ = (
        Index("ix_permission_scope", "user_id", "resource_type", "resource_id"),
    )
