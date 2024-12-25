from sqlalchemy.orm import Session
from src.models.template_3.jobs import Jobs
from src.repositories.base import BaseRepository


class JobsRepository(BaseRepository[Jobs]):
    def __init__(self, session: Session):
        super().__init__(Jobs, session)
