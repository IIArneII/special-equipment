from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from loguru import logger

from app.controllers.utils.responses import OK, NOT_FOUND
from app.services.users import UsersService
from app.container import Container


users_api = APIRouter(
    prefix='/users',
    tags=['users']
)

@users_api.get("/{id}")
@inject
def index(id: int, users_service: Provide[UsersService] = Depends(Provide[Container.users_service])):
    logger.info(f'{type(users_service)}')
    

    return '123'
