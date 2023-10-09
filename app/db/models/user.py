from app.db.models.base import SoftDeletedBaseModel
from app.services.enums.users import Role

from sqlalchemy import Column, String, Enum


class User(SoftDeletedBaseModel):
    __tablename__ = 'users'

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, server_default=Role.client)
    password_hash = Column(String, nullable=False)
