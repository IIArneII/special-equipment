from app.services.enums.base import StrEnum


class Role(StrEnum):
    client = 'client'
    agent = 'agent'
    moderator = 'moderator'
    admin = 'admin'
