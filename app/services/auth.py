from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta

from app.services.errors import BadRequestError, NOT_FOUND_ERR, WRONG_PASS_ERR
from app.repositories.users import UsersRepository
from app.services.helpers.try_except import try_except
from app.services.models.auth import TokenPyload, Tokens
from app.services.models.users import UserEntityCreate, UserRegister, UserEntity, UserLogin
from config import AuthConfig


class AuthService:
    def __init__(self, users_repository: UsersRepository, auth_config: dict) -> None:
        self._users_repository: UsersRepository = users_repository
        self._auth_config: AuthConfig = AuthConfig(auth_config)
    
    @try_except
    def login(self, model: UserLogin) -> Tokens:
        user = self._users_repository.get_by_username(model.username)

        if user is None:
            raise NOT_FOUND_ERR
        
        # if not bcrypt.verify(user.password_hash, model.password):
        #     return WRONG_PASS_ERR

        return Tokens(
            access_token=self._create_access_token(str(user.id)),
            refresh_token=''
        )

        # return Tokens(access=token)
    
    def _create_access_token(self, sub: str) -> str:
        iat = datetime.utcnow()
        exp = iat + timedelta(seconds=self._auth_config.ACCESS_TOKEN_EXPIRE)

        return jwt.encode(TokenPyload(
            sub=sub,
            exp=exp,
            iat=iat,
        ).model_dump(), self._auth_config.SECRET_KEY, algorithm=self._auth_config.ALGORITHM)
