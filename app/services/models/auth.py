from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime


class TokenPyload(PydanticBaseModel):
    sub: str
    exp: datetime
    iat: datetime


class Tokens(PydanticBaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
