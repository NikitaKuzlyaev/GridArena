from datetime import datetime
from typing import Sequence, Tuple

from mako.testing.helpers import result_lines
from sqlalchemy import select, update, delete, and_, Row

from core.dependencies.repository import get_repository
from core.models import Contest, Permission
from core.models.permission import PermissionResourceType, PermissionActionType
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.contest import ContestId
from core.utilities.loggers.log_decorator import log_calls


class QuizFieldCRUDRepository(BaseCRUDRepository):
    ...



quiz_field_repo = get_repository(
    repo_type=QuizFieldCRUDRepository
)
