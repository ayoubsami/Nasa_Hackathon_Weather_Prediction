from fastapi import FastAPI
from app.api import routes

app = FastAPI(
    title="Will It Rain On My Parade API",
    version="1.0.0",
    description="API de prédiction météo pour NASA Space Apps Challenge 2025"
)

app.include_router(routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API backend opérationnelle"}
