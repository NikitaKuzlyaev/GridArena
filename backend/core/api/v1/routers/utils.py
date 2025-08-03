from datetime import datetime

import fastapi

from backend.core.schemas.base import BaseSchemaModel
from backend.core.utilities.server import get_server_time

router = fastapi.APIRouter(prefix="/utils", tags=["utils"])


class ServerTimeResponse(BaseSchemaModel):
    server_time: datetime


@router.get(
    path="/server-time",
    response_model=ServerTimeResponse,
    status_code=200,
)
async def server_time(
) -> ServerTimeResponse:
    current_time: datetime = get_server_time(with_server_timezone=True)

    result = ServerTimeResponse(
        server_time=current_time,
    )
    result = result.model_dump()

    return result
