from contextlib import contextmanager, AbstractContextManager
from pydantic import BaseModel
from typing import Callable
from config import DBConfig
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

from alembic import command
from alembic.config import Config

Base: BaseModel = declarative_base()

import app.db.models.base
import app.db.models.user


class DataBase:
    def __init__(self, config: dict) -> None:
        logger.info(f'Init data base')
        
        self._config = DBConfig(config)
        self._engine = create_engine(self._config.dsn(), pool_pre_ping=True)
        self._session_factory = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        ))

        Base.metadata.bind = self._engine

        self.ping()

        if self._config.APPLY_MIGRATIONS:
            self._apply_migrations()

    def _apply_migrations(self) -> None:
        logger.info('Apply migrations')
        
        alembic_cfg = Config(self._config.ALEMBIC_INI_PATH)
        configuration = alembic_cfg.get_section(alembic_cfg.config_ini_section, {})
        configuration["sqlalchemy.url"] = self._config.dsn()
        command.upgrade(alembic_cfg, "head")

    def ping(self):
        logger.info('Ping data base')

        with self._engine.connect() as connection: ...

    @contextmanager
    def get_session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            logger.error('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
            logger.debug('Session close')
