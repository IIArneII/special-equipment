from pydantic import BaseModel as PydanticBaseModel

from app.services.enums.auth import TokenType
from app.services.models.base import BaseModel
from app.services.enums.users import Role


class TokenPyload(PydanticBaseModel):
    sub: str
    exp: int
    iat: int
    role: Role
    token_type: TokenType


class Tokens(PydanticBaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserLogin(BaseModel):
    username: str
    password: str


class UserRefreshLogin(PydanticBaseModel):
    refresh_token: str
