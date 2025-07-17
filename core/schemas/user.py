from core.schemas.base import BaseSchemaModel


class SiteUserCreate(BaseSchemaModel):
    username: str
    password: str


class ContestUserCreate(BaseSchemaModel):
    domain_number: int
    username: str
    password: str


class UserOut(BaseSchemaModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseSchemaModel):
    access_token: str
    token_type: str


class RefreshToken(BaseSchemaModel):
    refresh_token: str
