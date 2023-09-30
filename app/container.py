from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton, Configuration

from config import Config
from app.db.db import DataBase
from app.repositories.users import UsersRepository
from app.services.users import UsersService


class Container(DeclarativeContainer):
    config: Config = Configuration()

    wiring_config = WiringConfiguration(modules=["app.services.users"])

    db: DataBase = Singleton(DataBase, config=config.db)
    
    users_repository = Factory(UsersRepository, get_session=db.provided.get_session)

    users_service = Factory(UsersService, users_repository=users_repository)
