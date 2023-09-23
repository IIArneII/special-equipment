from fastapi import APIRouter
from app.controllers.utils.responses import OK, NOT_FOUND 


users_api = APIRouter(
    prefix='/users',
    tags=['users']
)
