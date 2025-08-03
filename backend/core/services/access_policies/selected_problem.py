from backend.core.repository.crud.uow import UnitOfWork
from backend.core.schemas.permission import PermissionPromise
from backend.core.services.access_policies.problem_card import ProblemCardAccessPolicy


class SelectedProblemAccessPolicy(ProblemCardAccessPolicy):

    async def can_contestant_buy_problem_card(
            self,
            uow: UnitOfWork,
            user_id: int,
            problem_card_id: int,
            raise_if_none: bool = True,
    ) -> PermissionPromise | None:
        # Проверка исключительно прав доступа. Без сложной бизнес-логики.
        # Считаем, что права есть тогда, когда есть права на просмотр связанной problem_card

        permission: PermissionPromise = (
            await self.can_contestant_view_problem_card(
                uow=uow, user_id=user_id, problem_card_id=problem_card_id, raise_if_none=raise_if_none)
        )
        return permission
