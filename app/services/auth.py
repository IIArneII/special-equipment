from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

from app.repositories.users import UsersRepository
from app.services.helpers.try_except import try_except
from app.services.models.errors import NOT_FOUND_ERR, WRONG_PASS_ERR, CREDENTIALS_ERR
from app.services.enums.users import Role
from app.services.enums.auth import TokenType
from app.services.models.auth import TokenPyload, Tokens, UserLogin, UserRefreshLogin
from config import AuthConfig


class AuthService:
    def __init__(self, users_repository: UsersRepository, auth_config: dict) -> None:
        self._users_repository: UsersRepository = users_repository
        self._auth_config: AuthConfig = AuthConfig(auth_config)
    
    @try_except
    def login(self, model: UserLogin) -> Tokens:
        user = self._users_repository.get_by_username_with_password(model.username)

        if user is None:
            raise NOT_FOUND_ERR
        
        if not bcrypt.verify(model.password, user.password_hash):
            raise WRONG_PASS_ERR

        return Tokens(
            access_token=self._create_access_token(str(user.id), user.role),
            refresh_token=self._create_refresh_token(str(user.id), user.role)
        )

    @try_except
    def refresh_login(self, model: UserRefreshLogin) -> Tokens:
        try:
            payload = TokenPyload.model_validate(jwt.decode(model.refresh_token, self._auth_config.SECRET_KEY, self._auth_config.ALGORITHM))
        except (JWTError, ValidationError):
            raise CREDENTIALS_ERR

        if payload.token_type != TokenType.refresh:
            raise CREDENTIALS_ERR

        user = self._users_repository.get(int(payload.sub))

        if user is None:
            raise CREDENTIALS_ERR
        
        # TODO: Хранить рефреш токены в бд и проверять, что совпадают

        return Tokens(
            access_token=self._create_access_token(str(user.id), user.role),
            refresh_token=self._create_refresh_token(str(user.id), user.role)
        )
            
    
    def _create_access_token(self, user: str, role: Role) -> str:
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(seconds=self._auth_config.ACCESS_TOKEN_EXPIRE)

        return jwt.encode(TokenPyload(
            sub=user,
            role=role,
            exp=int(exp.timestamp()),
            iat=int(iat.timestamp()),
            token_type=TokenType.access
        ).model_dump(), self._auth_config.SECRET_KEY, algorithm=self._auth_config.ALGORITHM)
    
    def _create_refresh_token(self, user: str, role: Role) -> str:
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(seconds=self._auth_config.REFRESH_TOKEN_EXPIRE)

        return jwt.encode(TokenPyload(
            sub=user,
            role=role,
            exp=int(exp.timestamp()),
            iat=int(iat.timestamp()),
            token_type=TokenType.refresh
        ).model_dump(), self._auth_config.SECRET_KEY, algorithm=self._auth_config.ALGORITHM)


# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjk3MjkxMDc1LCJpYXQiOjE2OTcyODc0NzUsInJvbGUiOiJjbGllbnQiLCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.W_wEZT7eV1rc7sjmOhY3312Z7kVxSMrbWXAR9uWeFLY",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjk3MzczODc1LCJpYXQiOjE2OTcyODc0NzUsInJvbGUiOiJjbGllbnQiLCJ0b2tlbl90eXBlIjoicmVmcmVzaCJ9.3kkWgO1VWsE_79OVc8ycgbjM6T3JWPvDYwDse6o9Z5E",
#   "token_type": "bearer"
# }