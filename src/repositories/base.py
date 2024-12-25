from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def find_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def find_all(self) -> List[T]:
        stmt = select(self.model)
        return list(self.session.execute(stmt).scalars().all())

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, id: int, **kwargs) -> Optional[T]:
        stmt = update(self.model).where(self.model.id == id).values(**kwargs)
        self.session.execute(stmt)
        self.session.commit()
        return self.find_by_id(id)

    def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount > 0

    def soft_delete(self, id: int) -> Optional[T]:
        return self.update(id, deleted_at=datetime.now())
