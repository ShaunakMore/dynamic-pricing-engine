import pandas as pd
import random
from src.utils import processDates

def generateTemporalFeatures(base_market_trend,market_trend_factor,market_noise) -> list[dict[str,int | str]]:
  """
  Get dates from Jan 1 2024 to 31 Dec 2025 along with features -
  month: int,
  weekday: str,
  weekend: 0 if weekend else 1,
  season: str (season according to the Indian Subcontinent)
  """
  date_range = pd.date_range('2024-01-01','2025-12-31').to_list()
  temporal_features = list(map(lambda x: processDates(x,base_market_trend,market_trend_factor,market_noise),date_range))  
  
  return temporal_features

def generatePropertyFeatures(base_property_pricings,rating_price_factor,competitor_bias_const) -> dict[str, str | int | float]:
  """
  Function to generate property features for the properties
  """
  
  # Generate a random property type
  property_int = random.randint(0,2)
  property_type = ""
  
  if(property_int == 0):
    property_type = "Entire house"
  elif(property_int == 1):
    property_type = "Private room"
  else:
    property_type = "Luxury suite"
  
  # Generate a random base rating, amenities score and location score
  base_rating = random.randint(1,100)
  amenities_score = random.randint(1,10)
  location_score = random.randint(1,10)
  
  # Better aminities mean better rating so we use a
  # simple coorelation to factor in aminities score
  amenities_boost = 0
  if(amenities_score <= 3):
    amenities_boost = 30
  elif(3 < amenities_score <= 6):
    amenities_boost = 60
  else:
    amenities_boost = 90
  
  # A good location means a better rating so we use a
  # simple coorelation to factor in location score
  location_boost = 0
  if(location_score <= 3):
    location_boost = 30
  elif(3 < location_score <= 6):
    location_boost = 60
  else:
    location_boost = 90
  
  # Final rating will be out of 300 but will never be 300
  # since we only use a max boost of 90 so no rating is completely 5 star
  final_rating = base_rating + amenities_boost + location_boost
  
  final_norm_rating = (final_rating/280) * 5
  
  property_pricing = base_property_pricings[property_type] + (final_norm_rating - 3.5) * rating_price_factor
  
  competitor_bias = random.uniform(-competitor_bias_const, competitor_bias_const)
  
  return {
    'property_type': property_type,
    'rating': round(final_norm_rating,2),
    'amenities_score': amenities_score,
    'location_score': location_score,
    'base_price': round(property_pricing,2),
    'competitor_bias': competitor_bias
  }