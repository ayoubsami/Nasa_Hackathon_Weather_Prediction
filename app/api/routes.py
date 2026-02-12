from fastapi import APIRouter
from app.schemas.weather_request import WeatherRequest
from app.schemas.weather_response import WeatherResponse
from app.services.message_generator import generate_friendly_message
import random

router = APIRouter()

@router.post("/predict", response_model=WeatherResponse)
async def predict_weather(request: WeatherRequest):
    # Mock de prédiction pour le frontend
    rain_prob = random.uniform(5, 80)
    temp = random.uniform(15, 28)
    wind = random.uniform(5, 25)
    message = generate_friendly_message(rain_prob, temp, wind)
    return WeatherResponse(
        rain_probability=round(rain_prob, 2),
        temperature_avg=round(temp, 2),
        wind_speed_avg=round(wind, 2),
        friendly_message=message
    )
