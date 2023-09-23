from app.repositories.users import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self._users_repository = users_repository
    
    def get(self, _id: int):
        ...
