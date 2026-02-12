from pydantic import BaseModel

class WeatherResponse(BaseModel):
    rain_probability: float
    temperature_avg: float
    wind_speed_avg: float
    friendly_message: str
