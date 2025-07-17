from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from core.api.v1.routers import routers as routers_v1

app = FastAPI()

# Разрешённые источники (в разработке можно '*')
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


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#
#     openapi_schema = get_openapi(
#         title="My API",
#         version="1.0.0",
#         description="API with OAuth2 Password Flow",
#         routes=app.routes,
#     )
#
#     openapi_schema["components"]["securitySchemes"] = {
#         "OAuth2PasswordBearer": {
#             "type": "oauth2",
#             "flows": {
#                 "password": {
#                     "tokenUrl": "/api/v1/auth/login",
#                     "scopes": {}
#                 }
#             }
#         }
#     }
#
#     # Вешаем security requirement на все пути (если нужно)
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             method.setdefault("security", [{"OAuth2PasswordBearer": []}])
#
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi

# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
