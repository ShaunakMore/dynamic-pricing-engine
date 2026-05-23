from fastapi import FastAPI
from app.schemas.request_schemas import OccupancyPredictionRequest
from app.services.predictor import predict_occupancy_rate
import json
app = FastAPI(title="Dynamic Pricing Engine")

@app.get('/')
async def basic_route():
  return{
    'message':"Dynamic Pricing API"
  }

@app.get('/health')
async def health_route():
  return{
    "message": "Working perfectly."
  }
  
@app.post("/predict-occupancy")
async def predict_occupancy(payload: OccupancyPredictionRequest):
  occupancy_rate = predict_occupancy_rate(payload)
  return {
    "occupancy_rate": occupancy_rate
  }