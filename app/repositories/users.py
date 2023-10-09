from app.db.models.user import User
from app.services.models.users import UserEntity, UserEntityCreate, UserEntityWithPassword


from sqlalchemy.orm.session import Session
from typing import Callable


class UsersRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    def get(self, id: int) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.id == id and
                User.deleted_at is None
            ).first()

            return UserEntity.model_validate(user) if user else None
    

    def get_by_username_with_password(self, username: str) -> UserEntityWithPassword | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.username == username and
                User.deleted_at is None
            ).first()
        
            return UserEntityWithPassword.model_validate(user) if user else None


    def get_by_username(self, username: str) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.username == username and
                User.deleted_at is None
            ).first()
        
            return UserEntity.model_validate(user) if user else None
    

    def get_by_email(self, email: str) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.email == email and
                User.deleted_at is None
            ).first()

            return UserEntity.model_validate(user) if user else None
    

    def create(self, model: UserEntityCreate) -> UserEntity:
        with self._get_session() as session:
            user = User(**model.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return UserEntity.model_validate(user)
