from pydantic import BaseModel

class OccupancyPredictionRequest(BaseModel):
  property_id: str
  location_score: int
  amenitites_score: int
  season: str
  property_type: str
  nearby_event: int
  holiday: int
  rating: float
  demand: float
  competitor_price: float
  market_trend: float
  final_price: float
  