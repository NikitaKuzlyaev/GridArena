from core.schemas.base import BaseSchemaModel
from datetime import datetime
from typing import Optional

from pydantic import Field, validator, root_validator, model_validator


class PermissionId(BaseSchemaModel):
    permission_id: int

