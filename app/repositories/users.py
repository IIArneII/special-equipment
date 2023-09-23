from app.db.models.user import User

from sqlalchemy.orm.session import Session

class UsersRepository:
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session

    def get(self, _id: int) -> User:
        print(type(self._db_session))
        self._db_session.query(User).filter(User.id == _id).first()
        ...
