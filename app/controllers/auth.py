from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.helpers.responses import OK, NOT_FOUND, BAD_REQUEST
from app.controllers.helpers.services_providers import auth_service
from app.services.auth import AuthService
from app.services.models.auth import Tokens
from app.services.models.users import UserLogin


auth_api = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_api.post("/login", responses= OK | BAD_REQUEST | NOT_FOUND)
def login(model: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(auth_service)) -> Tokens:
    return auth_service.login(UserLogin(username=model.username, password=model.password))
