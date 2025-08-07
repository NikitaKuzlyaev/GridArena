from typing import (
    Sequence,
    Tuple,
    Optional,
    Dict,
    List,
)

from backend.core.models import (
    SelectedProblem,
    ProblemCard,
    Problem,
    Contest,
)
from backend.core.models.contest import ContestRuleType
from backend.core.models.selected_problem import SelectedProblemStatusType
from backend.core.models.submission import SubmissionVerdict
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.problem import ProblemInfoForContestant
from backend.core.schemas.selected_problem import (
    SelectedProblemId,
    SelectedProblemInfoForContestant,
    ArraySelectedProblemInfoForContestant,
    SelectedProblemBuyRequest,
)
from backend.core.services.access_policies.selected_problem import SelectedProblemAccessPolicy
from backend.core.services.interfaces.selected_problem import ISelectedProblemService
from backend.core.services.rules.submission_reward import calculate_max_submission_reward
from backend.core.utilities.exceptions.database import EntityAlreadyExists
from backend.core.utilities.exceptions.logic import PossibleLimitOverflow
from backend.core.utilities.loggers.log_decorator import log_calls
from backend.handlers.contestant_log_writer import ContestantLogWriter

MAX_NUMBER_OF_ATTEMPTS = 3  # todo: как-то по-другому это должно быть...


class SelectedProblemService(ISelectedProblemService):
    def __init__(
            self,
            uow: UnitOfWork,
            access_policy: Optional[SelectedProblemAccessPolicy] = None,
    ):
        self.uow = uow
        self.access_policy: SelectedProblemAccessPolicy = access_policy or SelectedProblemAccessPolicy()

    async def _get_wrong_attempts(
            self,
            selected_problem_ids: list[int],
    ) -> Dict[int, int]:
        async with self.uow:
            # Правила DEFAULT подразумевают X попыток на решение задачи
            wrong_attempts_map: dict[int, int] = (
                await self.uow.submission_repo.get_attempts_count_grouped_by_selected_problem_id(
                    selected_problem_ids=selected_problem_ids,
                    filter_by_verdict=[SubmissionVerdict.WRONG.value],
                )
            )
            return wrong_attempts_map

    async def _get_remaining_number_of_attempts_for_selected_problems(
            self,
            selected_problem_ids: list[int],
            max_number_of_attempts: int = 3,
    ) -> dict[int, int]:
        async with self.uow:
            # Правила DEFAULT подразумевают X попыток на решение задачи
            wrong_attempts_map: Dict[int, int] = (
                await self._get_wrong_attempts(selected_problem_ids=selected_problem_ids, )
            )
            attempts_by_selected_problem = {
                sp_id: max_number_of_attempts - wrong_attempts_map.get(sp_id, 0)
                for sp_id in selected_problem_ids
            }
            return attempts_by_selected_problem

    async def _get_possible_reward(
            self,
            selected_problem_with_problem_card: List[Tuple[SelectedProblem, ProblemCard]],
    ) -> Dict[int, int]:
        async with self.uow:
            wrong_attempts_map: dict[int, int] = (
                await self._get_wrong_attempts(
                    selected_problem_ids=[i[0].id for i in selected_problem_with_problem_card],
                )
            )
            possible_reward_by_selected_problem = {}
            for sp, pc in selected_problem_with_problem_card:
                if sp.status != SelectedProblemStatusType.ACTIVE:
                    continue
                possible_reward = calculate_max_submission_reward(
                    number_of_tries_before=wrong_attempts_map.get(sp.id, 0),
                    cost_of_problem_card=pc.category_price,
                    contest_rule_type=ContestRuleType.DEFAULT,
                )
                if possible_reward is not None:
                    possible_reward_by_selected_problem[sp.id] = possible_reward

            return possible_reward_by_selected_problem

    @log_calls
    async def get_contestant_selected_problems(
            self,
            user_id: int,
    ) -> ArraySelectedProblemInfoForContestant:
        async with self.uow:
            # Проверка прав не требуется. Все описано в логике ниже.
            # Пользователь не может получить чужую информацию в принципе, так как жестко привязан своим domain_number

            _, contestant, contest, _ = await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )

            rows: Sequence[Tuple[SelectedProblem, ProblemCard, Problem]] = (
                await self.uow.selected_problem_repo.get_selected_problem_with_problem_card_and_problem_of_contestant_by_id(
                    contestant_id=contestant.id, )  # todo: это за замечательное название метода? <3
            )

            attempts_by_selected_problem = {}
            possible_reward_by_selected_problem: Dict[int, int] = {}

            if contest.rule_type == ContestRuleType.DEFAULT:
                attempts_by_selected_problem: Dict[int, int] = (
                    await self._get_remaining_number_of_attempts_for_selected_problems(
                        selected_problem_ids=[i[0].id for i in rows],
                        max_number_of_attempts=MAX_NUMBER_OF_ATTEMPTS, )
                )
                possible_reward_by_selected_problem: Dict[int, int] = (
                    await self._get_possible_reward(selected_problem_with_problem_card=[(i[0], i[1]) for i in rows], )
                )

            res = self._map_array_selected_problem_info_for_contestant(
                rows, contest, attempts_by_selected_problem, possible_reward_by_selected_problem, )

            return res

    @log_calls
    async def buy_selected_problem(  # todo: метод перегружен. предпринять что-то для оптимизации
            self,
            user_id: int,
            data: SelectedProblemBuyRequest,
    ) -> SelectedProblemId:
        async with self.uow:
            await self.access_policy.can_contestant_buy_problem_card(
                uow=self.uow, user_id=user_id, problem_card_id=data.problem_card_id, raise_if_none=True, )

            user, contestant, contest, _ = await self.uow.domain_repo.get_contestant_full_context(user_id=user_id, )

            problem_card: ProblemCard = await self.uow.problem_card_repo.get_problem_card_by_id(
                problem_card_id=data.problem_card_id, )

            selected_problem: SelectedProblem | None = (
                await self.uow.selected_problem_repo.get_selected_problem_by_contestant_and_problem_card(
                    contestant_id=contestant.id,
                    problem_card_id=data.problem_card_id, )
            )
            if selected_problem:  # Пользователь не может купить такую же задачу повторно
                raise EntityAlreadyExists("Selected problem already exists")

            active_selected_problems: Sequence[SelectedProblem] = (
                await self.uow.selected_problem_repo.get_selected_problem_of_contestant_by_id(
                    contestant_id=contestant.id,
                    filter_by_status=[SelectedProblemStatusType.ACTIVE.value], )
            )

            # Пользователь не может покупать задачи, если у него их максимум или больше допустимого число
            #   Замечание: не исключается случай, когда пользователь может иметь задач больше допустимого
            #   - например, когда одна или несколько задач были возвращены пользователю менеджером
            if len(active_selected_problems) >= contest.number_of_slots_for_problems:
                raise PossibleLimitOverflow("Action Denied: possible limit overflow.")

            selected_problem: SelectedProblem = await self.uow.transaction_repo.buy_problem(
                contestant_id=contestant.id, problem_card_id=problem_card.id, )

            # Делаем лог
            async with ContestantLogWriter(uow=self.uow) as clw:  # Пишем логи
                contestant_id = selected_problem.contestant_id
                await clw.log_balance_decrease(contestant_id, problem_card.category_price, )
                await clw.log_add_selected_problem(
                    contestant_id, problem_card.category_name, problem_card.category_price, )

            res = SelectedProblemId(selected_problem_id=selected_problem.id, )
            return res

    @staticmethod
    def _map_array_selected_problem_info_for_contestant(
            rows: Sequence[Tuple[SelectedProblem, ProblemCard, Problem]],
            contest: Contest,
            attempts_by_selected_problem: Dict[int, int],
            possible_reward_by_selected_problem: Dict[int, int],
    ) -> ArraySelectedProblemInfoForContestant:

        res = ArraySelectedProblemInfoForContestant(
            body=[
                SelectedProblemInfoForContestant(
                    selected_problem_id=selected_problem.id,
                    problem_card_id=problem_card.id,
                    problem=ProblemInfoForContestant(
                        problem_id=problem.id,
                        statement=problem.statement,
                    ),
                    category_name=problem_card.category_name,
                    category_price=problem_card.category_price,
                    created_at=selected_problem.created_at,
                    attempts_remaining=attempts_by_selected_problem.get(selected_problem.id, None),
                    possible_reward=possible_reward_by_selected_problem.get(selected_problem.id, None),
                ) for selected_problem, problem_card, problem in rows if
                selected_problem.status == SelectedProblemStatusType.ACTIVE  # todo: это что? 0_0
            ],
            rule_type=contest.rule_type,
            max_attempts_for_problem=MAX_NUMBER_OF_ATTEMPTS if contest.rule_type == ContestRuleType.DEFAULT else None,
        )
        return res
