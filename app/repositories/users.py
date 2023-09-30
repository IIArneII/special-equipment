from app.db.models.user import User

from sqlalchemy.orm.session import Session
from typing import Callable
from loguru import logger

class UsersRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, _id: int) -> User:
        with self._get_session() as session:
            user = session.query(User).filter(User.id == _id).first()
            logger.info(f'User: {user}')
