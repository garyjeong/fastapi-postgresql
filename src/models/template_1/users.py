from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.configs.database import Base
from src.models.base import TimestampMixin


class Users(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "template_1"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
