from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from jose import JWTError, jwt
from loguru import logger

from app.services.models.users import Profile
from app.container import Container
from config import AuthConfig


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@inject
def get_user(token: str = Depends(oauth2_scheme), config: dict = Depends(Provide[Container.config.auth])) -> Profile:
    try:
        logger.info(type(token))
        logger.info(config)
        config:AuthConfig = AuthConfig(config)
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
        return Profile(id=payload['sub'])
    
    except JWTError as e:
        logger.info(e)
        raise credentials_exception


def profile(profile: Profile = Depends(get_user)) -> Profile:
    return profile
