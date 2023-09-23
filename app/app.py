from config import Config
from loguru import logger
from fastapi import FastAPI

from app.controllers.utils.responses import INTERNAL_SERVER_ERROR
from app.controllers.utils.exception_handlers import not_found_handler, bad_request_handler, internal_server_error_handler
from app.controllers.users import users_api
from app.services.errors import NotFoundError, BadRequestError
from app.db.db import init_db, apply_migrations
from app.container import Container


def create_app(config: Config):
    global_api = FastAPI(
        debug=config.app_config.APP_DEBUG,
        docs_url=None,
        redoc_url=None,
    )

    init_db(config.db_config)

    if config.db_config.DB_APPLY_MIGRATIONS:
        apply_migrations(config.db_config)

    _init_routes(global_api, config)

    container = Container()

    try:
        users_repository = container.users_repository()
        user = users_repository.get(2)
    except Exception as e:
        print(e)

    return global_api


def _init_routes(global_api: FastAPI, config: Config):
    logger.info('Routes initialization...')

    api_v1 = FastAPI(
        debug=config.app_config.APP_DEBUG,
        version=config.api_config.API_VERSION,
        title=f'{config.api_config.API_TITLE} V1',
        summary=config.api_config.API_SUMMARY,
        description=config.api_config.API_DESCRIPTION,
        docs_url='/openapi' if config.api_config.API_IS_VISIBLE else None,
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    api_v1.add_exception_handler(NotFoundError, not_found_handler)
    api_v1.add_exception_handler(BadRequestError, bad_request_handler)
    api_v1.add_exception_handler(Exception, internal_server_error_handler)

    api_v1.include_router(users_api)
    
    global_api.mount(f'{config.api_config.API_PREFIX}/v1', api_v1)
