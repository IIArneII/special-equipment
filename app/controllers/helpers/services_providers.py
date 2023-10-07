from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from app.services.users import UsersService
from app.container import Container


@inject
def users_service(users_service: UsersService  = Depends(Provide[Container.users_service])) -> UsersService:
    return users_service
