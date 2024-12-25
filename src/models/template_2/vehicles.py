from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.configs.database import Base
from src.models.base import TimestampMixin
from src.models.template_1.users import Users


class Vehicles(TimestampMixin, Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": "template_2"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("template_1.users.id")
    )
    user: Mapped[Users] = relationship(back_populates="vehicles")
