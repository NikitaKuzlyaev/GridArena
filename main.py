from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.api.v1.routers import routers as routers_v1

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://192.168.0.2:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],  # или ['GET', 'POST', ...]
    allow_headers=["*"],  # или ['Content-Type', 'Authorization']
)

for router in routers_v1:
    app.include_router(router=router, prefix="/api/v1")
