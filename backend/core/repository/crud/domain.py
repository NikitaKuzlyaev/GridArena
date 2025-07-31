from backend.core.repository.crud.base import BaseCRUDRepository


class DomainCRUDRepository(BaseCRUDRepository):
    ...


"""
Пример вызова

domain_repo = get_repository(
    repo_type=DomainCRUDRepository
)
"""
