from app.db.models.base import SoftDeletedBaseModel

from sqlalchemy import Column, Integer, String

class User(SoftDeletedBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"
