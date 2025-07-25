import fastapi
from starlette.responses import JSONResponse

router = fastapi.APIRouter(prefix="/ping", tags=["ping"])


@router.get("/")
async def ping(

) -> JSONResponse:
    return JSONResponse({"message": "pong!"})
