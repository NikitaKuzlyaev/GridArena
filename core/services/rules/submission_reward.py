from datetime import datetime, timedelta

from core.models.contest import ContestRuleType


def calculate_max_submission_reward(
        number_of_tries_before: int,
        cost_of_problem_card: int,
        contest_rule_type: ContestRuleType,
        time_contest_start: datetime | None = None,
        time_selected_problem_create: datetime | None = None,
) -> int:
    if contest_rule_type == ContestRuleType.DEFAULT:
        if number_of_tries_before == 0:
            return cost_of_problem_card * 2
        elif number_of_tries_before == 1:
            return cost_of_problem_card * 3 // 2
        elif number_of_tries_before == 2:
            return cost_of_problem_card
        else:
            return 0

    else:
        raise NotImplementedError("not DEFAULT rules not implemented yet")
