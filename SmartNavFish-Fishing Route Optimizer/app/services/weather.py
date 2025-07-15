from datetime import datetime, timedelta
from typing import Optional
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.weather import WeatherCache
from app.config import settings

class WeatherService:
    def __init__(self, db: Session):
        self.db = db

    def get_weather_data(self, lat: float, lon: float) -> dict:
        # Check cache first
        cached = self.db.query(WeatherCache).filter(
            WeatherCache.latitude.between(lat - 0.1, lat + 0.1),
            WeatherCache.longitude.between(lon - 0.1, lon + 0.1),
            WeatherCache.expires_at > datetime.utcnow()
        ).first()
        
        if cached:
            return cached.data
        
        # If not in cache, fetch from API
        try:
            # Fetch from OpenWeatherMap
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.NOAA_API_KEY}"
            weather_data = requests.get(weather_url).json()
            
            # Fetch tides data
            tides_url = f"https://www.worldtides.info/api/v2?heights&lat={lat}&lon={lon}&key={settings.WORLD_TIDES_API_KEY}"
            tides_data = requests.get(tides_url).json()
            
            combined_data = {
                "weather": weather_data,
                "tides": tides_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Cache the data
            new_cache = WeatherCache(
                location=f"{lat},{lon}",
                latitude=lat,
                longitude=lon,
                data=combined_data,
                expires_at=datetime.utcnow() + timedelta(hours=1)
            )
            self.db.add(new_cache)
            self.db.commit()
            
            return combined_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

    def get_water_conditions(self, lat: float, lon: float) -> dict:
        # This would typically call ocean-specific APIs
        # For demo, we'll return mock data
        return {
            "temperature": 28.5,  # Celsius
            "salinity": 35.2,    # PSU
            "wave_height": 1.2,   # meters
            "current_speed": 0.5, # m/s
            "current_direction": 120  # degrees
        }