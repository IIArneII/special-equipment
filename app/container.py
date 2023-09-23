from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Callable

from app.db.db import get_session
from app.repositories.users import UsersRepository
from app.services.users import UsersService


class Container(DeclarativeContainer):
    db_session = Callable(get_session)
    
    users_repository = Factory(UsersRepository, db_session=db_session)

    users_service = Factory(UsersService, users_repository=users_repository)
