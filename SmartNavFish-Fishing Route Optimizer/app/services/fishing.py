from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fishing import FishingZone, MarineProtectedArea
from app.utils.geospatial import point_in_polygon
import requests
from app.config import settings

class FishingService:
    def __init__(self, db: Session):
        self.db = db

    def get_fishing_zones(self) -> List[FishingZone]:
        return self.db.query(FishingZone).all()

    def get_marine_protected_areas(self) -> List[MarineProtectedArea]:
        return self.db.query(MarineProtectedArea).all()

    def check_location_restrictions(self, lat: float, lng: float) -> dict:
        # Check against marine protected areas
        protected_areas = self.get_marine_protected_areas()
        restrictions = []
        
        for area in protected_areas:
            if point_in_polygon(lng, lat, area.coordinates['coordinates'][0]):
                restrictions.append({
                    'name': area.name,
                    'restrictions': area.restrictions,
                    'authority': area.authority
                })
        
        return {'in_restricted_area': len(restrictions) > 0, 'restrictions': restrictions}

    def get_species_distribution(self, species: Optional[str] = None):
        # This would typically call an external API or use ML model
        # For demo, we'll return mock data
        return {
            "species": species or "general",
            "distribution": [
                {"lat": 9.9312, "lng": 76.2673, "density": 0.8},
                {"lat": 9.9415, "lng": 76.2897, "density": 0.6},
            ]
        }

    def log_catch(self, user_id: int, data: dict):
        mongo_db = get_mongo_db()
        catch_data = {
            "user_id": user_id,
            "species": data.get("species"),
            "weight": data.get("weight"),
            "location": {
                "type": "Point",
                "coordinates": [data.get("longitude"), data.get("latitude")]
            },
            "timestamp": data.get("timestamp"),
            "gear_used": data.get("gear_used"),
            "weather_conditions": data.get("weather_conditions")
        }
        result = mongo_db.catches.insert_one(catch_data)
        return str(result.inserted_id)
