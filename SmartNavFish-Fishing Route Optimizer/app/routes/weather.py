from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.weather import WeatherService
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/weather")
def get_weather(lat: float, lon: float, db: Session = Depends(get_db)):
    service = WeatherService(db)
    return service.get_weather_data(lat, lon)

@router.get("/water-conditions")
def get_water_conditions(lat: float, lon: float, db: Session = Depends(get_db)):
    service = WeatherService(db)
    return service.get_water_conditions(lat, lon)