from pydantic import Field

from core.models import Contestant, User, ProblemCard, QuizField, Contest, Problem, SelectedProblem
from core.schemas.base import BaseSchemaModel


class BaseQuizContext(BaseSchemaModel):
    user: User
    contestant: Contestant
    quiz_field: QuizField
    contest: Contest


class UserContestantContext(BaseSchemaModel):
    user: User
    contestant: Contestant


class SelectedProblemContext(BaseSchemaModel):
    user: User
    contestant: Contestant
    selected_problem: SelectedProblem
    problem_card: ProblemCard
    problem: Problem

    def unpack(self) -> tuple[User, Contestant, SelectedProblem, ProblemCard, Problem]:
        return self.user, self.contestant, self.selected_problem, self.problem_card, self.problem