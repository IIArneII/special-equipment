from config import Config, LogConfig
from loguru import logger
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.dependencies.utils import get_typed_signature
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from fastapi.openapi.utils import get_openapi
from json import dumps, loads
from re import findall
import re

from app.controllers.helpers.responses import INTERNAL_SERVER_ERROR
from app.controllers.helpers import exception_handlers
from app.controllers.users import users_api
from app.controllers.auth import auth_api
from app.services.models.errors import NotFoundError, BadRequestError
from app.container import Container


def create_app(config: Config):
    _init_logger(config.log)

    container = Container()
    container.config.from_dict(config.model_dump())
    container.db()

    global_api = FastAPI(
        debug=config.app.DEBUG,
        docs_url=None,
        redoc_url=None,
    )
    global_api.container = container

    _init_routes(global_api, config)

    return global_api


def _init_logger(config: LogConfig):
    if config.TO_FILE:
        logger.add(f'{config.LOG_DIR}/logs.log', compression='zip', rotation=f'{config.ROTATION} MB', retention=config.RETENTION, level=config.LEVEL)


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

    api_v1.add_exception_handler(NotFoundError, exception_handlers.not_found_handler)
    api_v1.add_exception_handler(BadRequestError, exception_handlers.bad_request_handler)
    api_v1.add_exception_handler(HTTPException, exception_handlers.http_error_handler)
    api_v1.add_exception_handler(Exception, exception_handlers.internal_server_error_handler)

    api_v1.include_router(users_api)
    api_v1.include_router(auth_api)

    _build_openapi(api_v1)
    
    global_api.mount(f'{config.api.PREFIX}/v1', api_v1)


def _build_openapi(api: FastAPI):
    def _custom_openapi():
        if not api.openapi_schema:
            openapi_schema = get_openapi(
                title=api.title,
                version=api.version,
                openapi_version=api.openapi_version,
                summary=api.summary,
                description=api.description,
                terms_of_service=api.terms_of_service,
                contact=api.contact,
                license_info=api.license_info,
                routes=api.routes,
                webhooks=api.webhooks.routes,
                tags=api.openapi_tags,
                servers=api.servers,
                separate_input_output_schemas=api.separate_input_output_schemas,
            )
        
            api.openapi_schema = _fix_openapi(api, openapi_schema)
        
        return api.openapi_schema
    
    api.openapi = _custom_openapi


def _fix_openapi(api: FastAPI, schema: dict) -> dict:
        schema_json: str = dumps(schema)

        models_tytles = set(findall('Body_[\w]*"', schema_json))
        routes = list(filter(lambda x: isinstance(x, APIRoute), api.routes))

        for t in models_tytles:
            r: APIRoute = list(filter(lambda x: x.unique_id == t[5:-1:], routes))
            if not r:
                break
            r = r[0]

            endpoint_parameters = get_typed_signature(r.endpoint).parameters
            endpoint_parameters_names = list(endpoint_parameters.keys())
            if not endpoint_parameters_names:
                break

            annotation = endpoint_parameters[endpoint_parameters_names[0]].annotation
            if not issubclass(annotation, BaseModel):
                break

            schema_json = schema_json.replace(t, f'{annotation.__name__}"')
        
        models_tytles = set(findall('Body_[\w]*"', schema_json))
        if models_tytles:
            logger.warning(f'Uncorrected fields "Body_" detected: {", ".join([t[:-1] for t in models_tytles])}')
        
        openapi_schema = loads(schema_json)

        return openapi_schema
