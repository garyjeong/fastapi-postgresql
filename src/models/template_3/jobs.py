from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.configs.database import Base
from src.models.base import TimestampMixin
from src.models.template_1.users import Users
from src.models.template_2.vehicles import Vehicles


class Jobs(TimestampMixin, Base):
    __tablename__ = "jobs"
    __table_args__ = {"schema": "template_3"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("template_2.vehicles.id")
    )
    vehicle: Mapped[Vehicles] = relationship(back_populates="jobs")
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("template_1.users.id")
    )
    user: Mapped[Users] = relationship(back_populates="jobs")
