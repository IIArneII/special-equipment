from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import Form

from app.services.enums.base import StrEnum


class GrantType(StrEnum):
    password = 'password'
    refresh_token = 'refresh_token'


class Login(BaseModel):
    username: str | None = None
    password: str | None = None
    refresh_token: str | None = None
    grant_type: GrantType = GrantType.password

    def get_login(
            username: Annotated[str | None, Form()] = None,
            password: Annotated[str | None, Form(min_length=8)] = None,
            refresh_token: Annotated[str | None, Form()] = None,
            grant_type: GrantType = Form(GrantType.password)
        ):
        return Login(
            username=username,
            password=password,
            refresh_token=refresh_token,
            grant_type=grant_type,
        )
