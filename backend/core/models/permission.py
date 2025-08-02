import enum

from sqlalchemy import (
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from backend.core.database.connection import Base


class PermissionActionType(enum.Enum):
    """
    Тип действия разрешения. Описывает действие: что делать? - что пользователь авторизован делать?
    """

    ADMIN = "ADMIN"  # Полные права к ресурсу, включая все перечисленные ниже.
    EDIT = "EDIT"  # Право редактирования.


class PermissionResourceType(enum.Enum):
    """
    Тип ресурса разрешения. Описывает сущность: разрешение к чему? - к какому ресурсу относится разрешение?
    """

    DOMAIN = "DOMAIN"  # Домен. Это вся платформа. Осторожно! Выдача этого типа ресурса должна строго регулироваться.
    CONTEST = "CONTEST"  # Контест. Включает все связанные "нисходящие" сущности: quiz_field, problem_card, ...


class Permission(Base):
    __tablename__ = "permission"

    __table_args__ = (
        Index("idx_permission_scope", "user_id", "resource_type", "resource_id"),
        Index("idx_permission_id", "id"),
        Index("idx_permission_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )

    resource_type: Mapped[PermissionResourceType] = mapped_column(
        Enum(PermissionResourceType),
        nullable=False,
    )

    resource_id: Mapped[int] = mapped_column(
        nullable=True,
    )

    permission_type: Mapped[PermissionActionType] = mapped_column(
        Enum(PermissionActionType),
        nullable=False,
    )
