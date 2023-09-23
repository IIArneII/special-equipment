from contextlib import contextmanager
from config import DBConfig
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from alembic import command
from alembic.config import Config

Base = declarative_base()
_Session_maker: sessionmaker[Session] = None

import app.db.models.base
import app.db.models.user


def init_db(config: DBConfig):
    engine = create_engine(config.dsn())
    Base.metadata.bind = engine

    global _Session_maker
    _Session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def apply_migrations(config: DBConfig):
    alembic_cfg = Config("alembic.ini")
    configuration = alembic_cfg.get_section(alembic_cfg.config_ini_section, {})
    configuration["sqlalchemy.url"] = config.dsn()
    command.upgrade(alembic_cfg, "head")



async def get_session() -> Session:
    session = _Session_maker()
    try:
        yield session
    finally:
        session.close()
        logger.info('session close')
