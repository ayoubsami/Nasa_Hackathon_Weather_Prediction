from pydantic import BaseModel, Field
from datetime import date

class WeatherRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    event_date: date = Field(..., description="Date de l'événement (YYYY-MM-DD)")
