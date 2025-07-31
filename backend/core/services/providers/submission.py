from fastapi import Depends

from backend.core.repository.crud.uow import (
    UnitOfWork,
    get_unit_of_work,
)
from backend.core.services.domain.submission import SubmissionService
from backend.core.services.interfaces.submission import ISubmissionService


def get_submission_service(
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> ISubmissionService:
    return SubmissionService(
        uow=uow,
    )
