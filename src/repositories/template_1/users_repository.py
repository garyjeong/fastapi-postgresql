from sqlalchemy.orm import Session
from src.models.template_1.users import Users
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[Users]):
    def __init__(self, session: Session):
        super().__init__(Users, session)
