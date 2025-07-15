from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class FishingZone(Base):
    __tablename__ = "fishing_zones"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String, index=True)
    coordinates = Column(JSON)  # GeoJSON format
    fish_species = Column(JSON)  # List of common species
    restrictions = Column(JSON)  # Any fishing restrictions
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarineProtectedArea(Base):
    __tablename__ = "marine_protected_areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    coordinates = Column(JSON)  # GeoJSON format
    restrictions = Column(String)
    authority = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())