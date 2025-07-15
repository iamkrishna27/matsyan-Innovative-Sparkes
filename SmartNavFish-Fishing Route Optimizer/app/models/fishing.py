from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class FishingZone(Base):
    __tablename__ = "fishing_zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, index=True)
    coordinates = Column(JSON)
    fish_species = Column(JSON)
    restrictions = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarineProtectedArea(Base):
    __tablename__ = "marine_protected_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    coordinates = Column(JSON)
    restrictions = Column(String)
    authority = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
