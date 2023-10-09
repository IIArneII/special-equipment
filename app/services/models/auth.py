from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime

from app.services.enums.users import Role


class TokenPyload(PydanticBaseModel):
    sub: str
    exp: datetime
    iat: datetime
    role: Role


class Tokens(PydanticBaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
