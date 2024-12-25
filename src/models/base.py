from datetime import datetime

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all models."""

    id: any
    metadata: MetaData

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    metadata = MetaData(naming_convention=convention)


class TimestampMixin:
    """Mixin for created at Timestamp Field."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, comment="생성일시"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="수정일시",
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, comment="삭제일시"
    )

    def remove(self) -> None:
        self.deleted_at = datetime.now()
