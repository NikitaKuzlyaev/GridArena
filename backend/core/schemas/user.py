from enum import Enum

from backend.core.schemas.base import BaseSchemaModel


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


class UserType(str, Enum):
    SITE = "SITE"
    CONTEST = "CONTEST"


class Token(BaseSchemaModel):
    access_token: str
    token_type: str
    user_type: UserType


class RefreshToken(BaseSchemaModel):
    refresh_token: str
