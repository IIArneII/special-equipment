from app.services.models.base import BaseModel, EntityBaseModel, Page, Filter
from pydantic import Field, EmailStr
from fastapi import Depends


class UserEntity(EntityBaseModel):
    username: str
    email: EmailStr
    name: str


class UserEntityCreate(BaseModel):
    username: str
    email: EmailStr
    name: str
    password_hash: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class Profile(BaseModel):
    id: int = Field(ge=1)
