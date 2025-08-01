from typing import (
    Tuple,
    Optional,
)

from backend.core.models import (
    ProblemCard,
    Problem,
    QuizField,
)
from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.schemas.problem import ProblemInfoForEditor
from backend.core.schemas.problem_card import (
    ProblemCardId,
    ProblemCardInfoForEditor,
)
from backend.core.services.access_policies.problem_card import ProblemCardAccessPolicy
from backend.core.services.interfaces.problem_card import IProblemCardService
from backend.core.utilities.exceptions.database import EntityDoesNotExist
from backend.core.utilities.loggers.log_decorator import log_calls


class ProblemCardService(IProblemCardService):
    def __init__(
            self,
            uow: UnitOfWork,
            access_policy: Optional[ProblemCardAccessPolicy] = None,
    ):
        self.uow = uow
        self.access_policy: ProblemCardAccessPolicy = access_policy or ProblemCardAccessPolicy()

    @log_calls
    async def create_problem_card_with_problem(
            self,
            user_id: int,
            quiz_field_id: int,
            row: int,
            column: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            permission: PermissionPromise = (
                await self.access_policy.can_user_edit_quiz_field(
                    uow=self.uow, user_id=user_id, quiz_field_id=quiz_field_id, raise_if_none=True, ))

            quiz_field: QuizField = (
                await self.uow.quiz_field_repo.get_quiz_field_by_id(
                    quiz_field_id=quiz_field_id, )
            )  # Существование quiz_field проверено в access_policy

            problem_card_with_problem: Tuple[ProblemCard, Problem] = (
                await self.uow.problem_card_repo.create_problem_card_with_problem(
                    quiz_field_id=quiz_field_id,
                    row=row,
                    column=column,
                    category_name=category_name,
                    category_price=category_price,
                    statement=statement,
                    answer=answer,
                )
            )
            problem_card, _ = problem_card_with_problem
            res = ProblemCardId(
                problem_card_id=problem_card.id,
            )
            return res

    @log_calls
    async def update_problem_card_with_problem(
            self,
            user_id: int,
            problem_card_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            permission: PermissionPromise = (
                await self.access_policy.can_user_edit_problem_card(
                    uow=self.uow, user_id=user_id, problem_card_id=problem_card_id, raise_if_none=True, ))

            problem_card: ProblemCard = (
                await self.uow.problem_card_repo.update_problem_card_with_problem(
                    problem_card_id=problem_card_id,
                    problem_id=problem_id,
                    category_name=category_name,
                    category_price=category_price,
                    statement=statement,
                    answer=answer, )
            )  # Существование problem_card проверено в access_policy

            res = ProblemCardId(
                problem_card_id=problem_card.id,
            )
            return res

    @log_calls
    async def problem_card_info_for_editor(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> ProblemCardInfoForEditor:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            permission: PermissionPromise = (
                await self.access_policy.can_user_edit_problem_card(
                    uow=self.uow, user_id=user_id, problem_card_id=problem_card_id, raise_if_none=True, ))

            problem_card_with_problem: Tuple[ProblemCard, Problem] | None = (
                await self.uow.problem_card_repo.get_tuple_problem_card_with_problem_by_problem_card_id(
                    problem_card_id=problem_card_id, )
            )
            if not problem_card_with_problem:
                raise EntityDoesNotExist("ProblemCard not found")

            problem_card, problem = problem_card_with_problem

            res = ProblemCardInfoForEditor(
                problem_card_id=problem_card.id,
                problem=ProblemInfoForEditor(
                    problem_id=problem.id,
                    statement=problem.statement,
                    answer=problem.answer,
                ),
                row=problem_card.row,
                column=problem_card.column,
                category_price=problem_card.category_price,
                category_name=problem_card.category_name,
            )
            return res

    @log_calls
    async def create_problem_card(
            self,
            user_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            quiz_field_id: int,
            row: int,
            column: int,
    ) -> ProblemCardId:
        async with self.uow:
            # Проверка прав доступа к ресурсу. Если доступа нет - выбросится исключение (raise_if_none=True)
            permission: PermissionPromise = (
                await self.access_policy.can_user_edit_quiz_field(
                    uow=self.uow, user_id=user_id, quiz_field_id=quiz_field_id, raise_if_none=True, ))

            problem_card: ProblemCard = (
                await self.uow.problem_card_repo.create_problem_card(
                    problem_id=problem_id,
                    category_name=category_name,
                    category_price=category_price,
                    quiz_field_id=quiz_field_id,
                    row=row,
                    column=column,
                )
            )
            res = ProblemCardId(
                problem_card_id=problem_card.id,
            )
            return res

    @log_calls
    async def update_problem_card(
            self,
            user_id: int,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCardId:
        raise NotImplementedError("method not implemented")
