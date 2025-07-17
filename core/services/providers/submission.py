from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.submission import SubmissionCRUDRepository
from core.services.domain.submission import SubmissionService
from core.services.interfaces.submission import ISubmissionService


def get_submission_service(
        submission_repo: SubmissionCRUDRepository = Depends(get_repository(SubmissionCRUDRepository)),
) -> ISubmissionService:
    return SubmissionService(
        submission_repo=submission_repo,
    )
