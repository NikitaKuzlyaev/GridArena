from sqlalchemy import update, select

from core.dependencies.repository import get_repository
from core.models import SelectedProblem, Contestant, ProblemCard, Contest, User
from core.models.selected_problem import SelectedProblemStatusType
from core.models.submission import Submission
from core.repository.crud.base import BaseCRUDRepository
from core.utilities.loggers.log_decorator import log_calls


class TransactionCRUDRepository(BaseCRUDRepository):

    @log_calls
    async def create_submission(
            self,
            contestant_id: int,
            selected_problem_id: int,
            verdict: str,
            points_delta: int,
    ) -> Submission:
        ...

    @log_calls
    async def buy_problem(
            self,
            contestant_id: int,
            problem_card_id: int,
    ) -> SelectedProblem:
        try:
            res = await self.async_session.execute(
                select(Contestant).where(Contestant.id == contestant_id)
            )
            contestant = res.scalar_one_or_none()

            res = await self.async_session.execute(
                select(ProblemCard).where(ProblemCard.id == problem_card_id)
            )
            problem_card = res.scalar_one_or_none()

            if contestant is None or problem_card is None:
                raise ValueError("Invalid contestant or problem card")

            res = await self.async_session.execute(
                select(
                    Contest
                )
                .join(
                    User, User.domain_number == Contest.id
                )
                .join(
                    Contestant, Contestant.user_id == User.id
                )
                .where(
                    Contestant.id == contestant.id
                )
            )
            contest = res.scalar_one_or_none()

            if (contestant.points < problem_card.category_price and
                    not contest.flag_user_can_have_negative_points):
                raise ValueError("Not enough points")

            await self.async_session.execute(
                update(Contestant)
                .where(Contestant.id == contestant_id)
                .values(points=contestant.points - problem_card.category_price)
                .execution_options(synchronize_session="fetch")
            )

            selected_problem = SelectedProblem(
                problem_card_id=problem_card_id,
                contestant_id=contestant_id,
                status=SelectedProblemStatusType.ACTIVE,
            )
            self.async_session.add(selected_problem)

            await self.async_session.commit()
            await self.async_session.refresh(selected_problem)
            return selected_problem

        except Exception:
            await self.async_session.rollback()
            raise


transaction_repo = get_repository(
    repo_type=TransactionCRUDRepository
)
