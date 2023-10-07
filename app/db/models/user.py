from app.db.models.base import SoftDeletedBaseModel
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String

class User(SoftDeletedBaseModel):
    __tablename__ = 'users'

    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
