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


class ContestCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_contest(
            self,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> Contest:
        new_contest: Contest = (
            Contest(
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
            )
        )
        self.async_session.add(instance=new_contest)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_contest)
        return new_contest

    @log_calls
    async def update_contest(
            self,
            contest_id: int,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> Contest | None:
        await self.async_session.execute(
            update(
                Contest
            )
            .where(
                Contest.id == contest_id,
            )
            .values(
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
            )
            .execution_options(
                synchronize_session="fetch"
            )
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(
                Contest
            ).where(
                Contest.id == contest_id,
            )
        )
        return result.scalar_one_or_none()

    @log_calls
    async def get_user_contests(
            self,
            user_id: int,
    ) -> Sequence[Contest]:
        rows = await self.async_session.execute(
            select(
                Contest,
            )
            .join(
                Permission,
                and_(
                    Permission.user_id == user_id,
                    Permission.resource_type == PermissionResourceType.CONTEST.value,
                    Permission.resource_id == Contest.id,
                    Permission.permission_type == PermissionActionType.EDIT.value,
                )
            )
        )
        result = rows.scalars().all()
        return result


contest_repo = get_repository(
    repo_type=ContestCRUDRepository
)
