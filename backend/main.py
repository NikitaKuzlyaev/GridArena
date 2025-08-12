import os

from fastapi import (
    FastAPI,
    Request,
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pyinstrument import Profiler
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from backend.core.api.v1.routers import routers as routers_v1
from backend.metrics.middleware import MetricsMiddleware

app = FastAPI(root_path='/api')

origins = [
    "http://localhost:5173",
    "http://192.168.0.2:5173",
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],  # или ['GET', 'POST', ...]
    allow_headers=["*"],  # или ['Content-Type', 'Authorization']
)

app.add_middleware(MetricsMiddleware)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# @app.middleware("http")
# Для профилирования
async def profile_request(request: Request, call_next):
    profiler = Profiler()
    profiler.start()

    response = await call_next(request)

    profiler.stop()

    # Папка для профилей
    profiles_dir = "../profiles"
    os.makedirs(profiles_dir, exist_ok=True)

    safe_path = request.url.path.strip("/").replace("/", "_") or "root"
    filename = f"profile_{safe_path}.html"
    filepath = os.path.join(profiles_dir, filename)

    with open(filepath, "w") as f:
        f.write(profiler.output_html())

    print(f"[PyInstrument] Профиль сохранён: {filepath}")

    return response


for router in routers_v1:
    app.include_router(router=router, prefix="/v1")


# uvicorn backend.main:app --host 0.0.0.0 --port 8000
# uvicorn backend.main:app --host localhost --port 8000
# uvicorn backend.main:app --host 127.0.0.1 --port 8000