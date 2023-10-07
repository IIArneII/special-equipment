from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.controllers.helpers.models import Error
from app.services.errors import NotFoundError, BadRequestError

def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Error(message=str(exc)).model_dump(),
    )

def bad_request_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=Error(message=str(exc)).model_dump(),
    )

def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Error(message=str(exc)).model_dump(),
    )
