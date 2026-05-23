from fastapi import FastAPI
from app.schemas.request_schemas import OccupancyPredictionRequest
from app.services.predictor import predict_occupancy_rate,optimize_pricing
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
  occupancy_rate,prediction_df = predict_occupancy_rate(payload)
  optimized_price = optimize_pricing(prediction_df=prediction_df)[0][0]
  return {
    "occupancy_rate": occupancy_rate,
    "optimized_price":optimized_price
  }