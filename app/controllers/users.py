from fastapi import APIRouter, Depends

from app.controllers.helpers.responses import OK, NOT_FOUND, BAD_REQUEST
from app.controllers.helpers.services_providers import users_service
from app.services.users import UsersService
from app.services.models.users import UserRegister, UserEntity


users_api = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_api.post("/register", responses= OK | BAD_REQUEST)
def register(model: UserRegister, users_service: UsersService = Depends(users_service)) -> UserEntity:
    return users_service.register(model)


@users_api.get("/{id}", responses= OK | NOT_FOUND)
def get(id: int, users_service: UsersService = Depends(users_service)) -> UserEntity:
    return users_service.get(id)
