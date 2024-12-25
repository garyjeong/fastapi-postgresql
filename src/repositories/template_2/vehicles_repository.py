from sqlalchemy.orm import Session
from src.models.template_2.vehicles import Vehicles
from src.repositories.base import BaseRepository


class VehicleRepository(BaseRepository[Vehicles]):
    def __init__(self, session: Session):
        super().__init__(Vehicles, session)
