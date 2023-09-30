from app.repositories.users import UsersRepository
from app.services.errors import NotFoundError


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self._users_repository = users_repository
    
    def get(self, _id: int):
        self._users_repository.get(_id)
        raise NotFoundError(f'User {_id} not found')
