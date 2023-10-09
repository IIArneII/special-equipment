from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from jose import JWTError, jwt

from app.controllers.helpers.exceptions import CREDENTIALS_ERR, FORBIDDEN_ERR
from app.services.enums.users import Role
from app.services.models.users import UserEntity
from app.services.errors import NotFoundError
from app.services.users import UsersService
from app.container import Container


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@inject
def get_user(
    token: str = Depends(oauth2_scheme),
    config: dict = Depends(Provide[Container.config.auth]),
    user_service: UsersService = Depends(Provide[Container.users_service])
    ) -> UserEntity:
    try:
        payload = jwt.decode(token, config['SECRET_KEY'], algorithms=config['ALGORITHM'])
        
        if (id := payload.get('sub')) is None:
            raise CREDENTIALS_ERR

        return user_service.get(int(id))
    
    except (JWTError, NotFoundError) as e:
        raise CREDENTIALS_ERR


class Profile:
    def __init__(self, roles: list[Role] = []) -> None:
        self.roles = roles

    def __call__(self, profile: UserEntity = Depends(get_user)) -> UserEntity:
        if self.roles and profile.role not in self.roles:
            raise FORBIDDEN_ERR
        
        return profile
