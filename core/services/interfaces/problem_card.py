from typing import Protocol

from core.schemas.problem_card import ProblemCardId, ProblemCardInfoForEditor


class IProblemCardService(Protocol):

    async def create_problem_card_with_problem(
            self,
            quiz_field_id: int,
            row: int,
            column: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        ...

    async def update_problem_card_with_problem(
            self,
            problem_card_id: int,
            problem_id: int,
            category_name: str,
            category_price: int,
            statement: str,
            answer: str,
    ) -> ProblemCardId:
        ...

    async def create_problem_card(
            self,
            problem_id: int,
            category_name: str,
            category_price: int,
            quiz_field_id: int,
            row: int,
            column: int,
    ) -> ProblemCardId:
        ...

    async def update_problem_card(
            self,
            problem_card_id: int,
            category_name: str,
            category_price: int,
    ) -> ProblemCardId:
        ...

    async def problem_card_info_for_editor(
            self,
            user_id: int,
            problem_card_id: int,
    ) -> ProblemCardInfoForEditor:
        ...
