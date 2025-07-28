from backend.core.schemas.base import BaseSchemaModel


class PermissionId(BaseSchemaModel):
    permission_id: int


class PermissionPromise(BaseSchemaModel):
    message: str | None = None
