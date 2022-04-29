from sqlalchemy import Column, Integer, String, Float

from .base import Base


class Metrobus(Base):
    __tablename__ = 'metrobus'

    vehicle_id = Column(Integer, primary_key=True, unique=True)
    vehicle_label = Column(Integer)
    vehicle_current_status = Column(Integer)
    position_latitude = Column(Float(10, 15))
    position_longitude = Column(Float(10, 15))
    county = Column(String(100))

    def __init__(self, vehicle_id, vehicle_label, vehicle_current_status, position_latitude, position_longitude, county):

        self.vehicle_id = vehicle_id
        self.vehicle_label = vehicle_label
        self.vehicle_current_status = vehicle_current_status
        self.position_latitude = position_latitude
        self.position_longitude = position_longitude
        self.county = county