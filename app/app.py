from config import Config
from loguru import logger
from fastapi import FastAPI

from app.controllers.utils.responses import INTERNAL_SERVER_ERROR
from app.controllers.utils.exception_handlers import not_found_handler, bad_request_handler, internal_server_error_handler
from app.controllers.users import users_api
from app.services.errors import NotFoundError, BadRequestError
from app.container import Container


def create_app(config: Config):
    container = Container()
    container.config.from_dict(config.model_dump())

    global_api = FastAPI(
        debug=config.app.DEBUG,
        docs_url=None,
        redoc_url=None,
    )
    global_api.container = container

    _init_routes(global_api, config)

    return global_api


def _init_routes(global_api: FastAPI, config: Config):
    logger.info('Routes initialization...')

    api_v1 = FastAPI(
        debug=config.app.DEBUG,
        version=config.api.VERSION,
        title=f'{config.api.TITLE} V1',
        summary=config.api.SUMMARY,
        description=config.api.DESCRIPTION,
        docs_url='/openapi' if config.api.IS_VISIBLE else None,
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    api_v1.add_exception_handler(NotFoundError, not_found_handler)
    api_v1.add_exception_handler(BadRequestError, bad_request_handler)
    api_v1.add_exception_handler(Exception, internal_server_error_handler)

    api_v1.include_router(users_api)
    
    global_api.mount(f'{config.api.PREFIX}/v1', api_v1)
