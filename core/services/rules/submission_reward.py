from datetime import datetime, timedelta

from core.models.contest import ContestRuleType


def calculate_max_submission_reward(
        number_of_tries_before: int,
        contest_rule_type: ContestRuleType,
        time_contest_start: datetime | None = None,
        time_selected_problem_create: datetime | None = None,
) -> int:

    if contest_rule_type == ContestRuleType.DEFAULT:
        ...

    else:
        raise NotImplementedError("not DEFAULT rules not implemented yet")
