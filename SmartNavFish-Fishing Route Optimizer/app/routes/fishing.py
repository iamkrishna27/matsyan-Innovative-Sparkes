from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.fishing import FishingService
from app.services.auth import get_current_user
from app.models.user import User
from typing import List, Optional
from pydantic import BaseModel
import datetime

router = APIRouter()

class FishingZoneResponse(BaseModel):
    id: int
    zone_name: str
    coordinates: dict
    fish_species: list
    restrictions: Optional[dict]

class CatchLog(BaseModel):
    species: str
    weight: float
    latitude: float
    longitude: float
    timestamp: datetime.datetime
    gear_used: Optional[str] = None
    weather_conditions: Optional[dict] = None

class LocationCheckResponse(BaseModel):
    in_restricted_area: bool
    restrictions: list

@router.get("/zones", response_model=List[FishingZoneResponse])
def get_fishing_zones(db: Session = Depends(get_db)):
    service = FishingService(db)
    return service.get_fishing_zones()

@router.get("/restrictions")
def check_location_restrictions(lat: float, lng: float, db: Session = Depends(get_db)):
    service = FishingService(db)
    return service.check_location_restrictions(lat, lng)

@router.get("/species-distribution")
def get_species_distribution(species: Optional[str] = None, db: Session = Depends(get_db)):
    service = FishingService(db)
    return service.get_species_distribution(species)

@router.post("/log-catch")
def log_catch(catch_data: CatchLog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = FishingService(db)
    return service.log_catch(current_user.id, catch_data.dict())

@router.get("/optimal-route")
def get_optimal_route(
    start_lat: float,
    start_lng: float,
    target_species: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from app.services.prediction import PredictionService
    prediction_service = PredictionService()
    return prediction_service.predict_optimal_routes(
        {"lat": start_lat, "lng": start_lng},
        datetime.datetime.now()
    )