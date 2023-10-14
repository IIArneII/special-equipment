from fastapi import APIRouter, Depends
from typing import Annotated

from app.controllers.helpers.responses import OK, NOT_FOUND, BAD_REQUEST
from app.controllers.helpers.exceptions import GRANT_TYPE_PASS_ERR, GRANT_TYPE_REFRESH_ERR
from app.controllers.helpers.services_providers import auth_service
from app.controllers.models.auth import Login, GrantType
from app.services.auth import AuthService
from app.services.models.auth import Tokens, UserLogin, UserRefreshLogin


auth_api = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_api.post("/login", responses= OK | BAD_REQUEST | NOT_FOUND)
def login(model: Login = Depends(Login.get_login), auth_service: AuthService = Depends(auth_service)) -> Tokens:
    if model.grant_type == GrantType.password and (model.username is None or model.password is None):
        raise GRANT_TYPE_PASS_ERR

    if model.grant_type == GrantType.refresh_token and model.refresh_token is None:
        raise GRANT_TYPE_REFRESH_ERR
    
    if model.grant_type == GrantType.password:
        return auth_service.login(UserLogin(username=model.username, password=model.password))

    return auth_service.refresh_login(UserRefreshLogin(refresh_token=model.refresh_token))
