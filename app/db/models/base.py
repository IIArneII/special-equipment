from app.db.db import Base

from sqlalchemy import Column, Integer, DateTime
from datetime import datetime


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SoftDeletedBaseModel(BaseModel):
    __abstract__ = True

    deleted_at = Column(DateTime, nullable=True)
