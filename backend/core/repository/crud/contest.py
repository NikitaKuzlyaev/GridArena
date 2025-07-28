from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update, delete, and_, func

from backend.core.dependencies.repository import get_repository
from backend.core.models import Contest, Permission, QuizField, ProblemCard, Problem, User, Contestant
from backend.core.models.permission import PermissionResourceType, PermissionActionType
from backend.core.repository.crud.base import BaseCRUDRepository
from backend.core.schemas.contest import ArrayContestantInStandings, ContestantInStandings
from backend.core.utilities.loggers.log_decorator import log_calls


class ContestCRUDRepository(BaseCRUDRepository):

    async def get_contestant_in_standings(
            self,
            contest_id: int,
    ) -> Sequence[ContestantInStandings]:
        res = await self.async_session.execute(
            select(
                Contestant.id.label("contestant_id"),
                Contestant.name,
                Contestant.points,
                func.rank().over(order_by=Contestant.points.desc()).label("rank")
            )
            .join(User, Contestant.user_id == User.id)
            .join(Contest, User.domain_number == Contest.id)
            .where(Contest.id == contest_id)
            .order_by(Contestant.points.desc())
        )

        rows = res.all()
        return [
            ContestantInStandings(
                contestant_id=row.contestant_id,
                name=row.name,
                points=row.points,
                rank=row.rank,
            )
            for row in rows
        ]

    async def delete_contest(
            self,
            contest_id: int,
    ) -> None:
        await self.async_session.execute(
            delete(Contest)
            .where(Contest.id == contest_id)
        )
        await self.async_session.commit()

    async def get_contest_by_user_id(
            self,
            user_id: int,
    ) -> Contest | None:
        res = await self.async_session.execute(
            select(Contest)
            .join(User, User.domain_number == Contest.id)
            .where(User.id == user_id)
        )
        return res.scalar_one_or_none()

    async def get_contest_by_id(
            self,
            contest_id: int,
    ) -> Contest | None:
        res = await self.async_session.execute(
            select(Contest)
            .where(Contest.id == contest_id)
        )
        return res.scalar_one_or_none()

    @log_calls
    async def create_full_contest(
            self,
            name: str,
            started_at: datetime,
            closed_at: datetime,
            start_points: int,
            number_of_slots_for_problems: int,
    ) -> Contest:
        contest = Contest(
            name=name,
            started_at=started_at,
            closed_at=closed_at,
            start_points=start_points,
            number_of_slots_for_problems=number_of_slots_for_problems,
        )
        self.async_session.add(contest)
        await self.async_session.flush()

        quiz_field = QuizField(
            contest_id=contest.id,
            number_of_rows=1,
            number_of_columns=1,
        )
        self.async_session.add(quiz_field)
        await self.async_session.flush()

        problem = Problem(
            statement="-",
            answer="-",
        )
        self.async_session.add(problem)
        await self.async_session.flush()

        problem_card = ProblemCard(
            problem_id=problem.id,
            category_name="cat",
            category_price=100,
            quiz_field_id=quiz_field.id,
            row=1,
            column=1,
        )
        self.async_session.add(problem_card)

        await self.async_session.refresh(contest)
        return contest

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
            rule_type: str,
            flag_user_can_have_negative_points: bool,
    ) -> Contest | None:
        await self.async_session.execute(
            update(Contest)
            .where(Contest.id == contest_id)
            .values(
                name=name,
                started_at=started_at,
                closed_at=closed_at,
                start_points=start_points,
                number_of_slots_for_problems=number_of_slots_for_problems,
                rule_type=rule_type,
                flag_user_can_have_negative_points=flag_user_can_have_negative_points,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(Contest)
            .where(Contest.id == contest_id)
        )
        return result.scalar_one_or_none()

    @log_calls
    async def get_user_contests(
            self,
            user_id: int,
    ) -> Sequence[Contest]:
        rows = await self.async_session.execute(
            select(Contest)
            .join(
                Permission,
                and_(
                    Permission.user_id == user_id,
                    Permission.resource_type == PermissionResourceType.CONTEST.value,
                    Permission.resource_id == Contest.id,
                    Permission.permission_type == PermissionActionType.EDIT.value,
                ))
        )
        result = rows.scalars().all()
        return result


contest_repo = get_repository(
    repo_type=ContestCRUDRepository
)
