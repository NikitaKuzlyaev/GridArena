from core.schemas.base import BaseSchemaModel


class SelectedProblemId(BaseSchemaModel):
    selected_problem_id: int


class SelectedProblemBuyRequest(BaseSchemaModel):
    problem_card_id: int
