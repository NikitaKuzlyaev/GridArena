import os

from fastapi import (
    FastAPI,
    Request,
)
from pyinstrument import Profiler
from starlette.middleware.cors import CORSMiddleware

from backend.core.api.v1.routers import routers as routers_v1

app = FastAPI(root_path='/api')

origins = [
    "http://localhost:5173",
    "http://192.168.0.2:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],  # или ['GET', 'POST', ...]
    allow_headers=["*"],  # или ['Content-Type', 'Authorization']
)


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
