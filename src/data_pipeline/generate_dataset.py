import pandas as pd
import random
import datetime
from typing import Annotated, Final
from annotated_doc import Doc
from math import exp

from src.feature_engineering import generateTemporalFeatures,generatePropertyFeatures

RANDOM_SEED = 42

NUM_PROPERTIES = 500

NUM_DATES = 500

BASE_BOOST = 25

SUMMER_SEASONAL_BOOST = 75

WINTER_SEASON_BOOST = 50

MONSOON_SEASON_BOOST = 25

EVENT_BOOST = 75

WEEKEND_BOOST = 50

HOLIDAY_BOOST = 75

BASE_PROPERTY_PRICINGS = { 
              "Entire house": 3000,
              "Private room": 1000,
              "Luxury suite": 2000
              }

RATING_DEMAND_FACTOR = 60

MARKET_TREND_FACTOR = 0.0005

BASE_MARKET_TREND = 1

MARKET_NOISE = 0.0005

DEMAND_NOISE = 0.1

DEMAND_PRICE_FACTOR = 800

RATING_PRICE_FACTOR = 100

MARKET_TREND_PRICE_FACTOR = 100

PRICE_NOISE = 50

COMPETITOR_BIAS = 0.1

COMPETITOR_NOISE = 100

PRICE_ELASTICITY_FACTOR = 20

QUALITY_BOOST_FACTOR = 0.8


def processTemporalAndPropertyFeatures(property_index:int, property_features: dict, temporal_features: dict) -> dict:
  """
  Processes the temporal and property features, and returns a complete feature dictionary.
  """
  
  # Extract all feature values
  property_id = f"P{property_index}"
  date = temporal_features['date']
  property_type = property_features['property_type']
  location_score = property_features['location_score']
  amenities_score = property_features['amenities_score']
  rating = property_features['rating']
  base_price = property_features['base_price']
  month = temporal_features['month']
  weekday = temporal_features['weekday']
  weekend = temporal_features['weekend']
  season = temporal_features['season']
  holiday = temporal_features['holiday']
  nearby_event = temporal_features['nearby_event']
  market_trend = temporal_features['market_trend']
  base_demand = 100 + (RATING_DEMAND_FACTOR * (rating/5))
  
  # Calculate demand 
  seasonal_demand_boost = 0
  if(season == "Summer"):
    seasonal_demand_boost = SUMMER_SEASONAL_BOOST
  elif(season == "Winter"):
    seasonal_demand_boost = WINTER_SEASON_BOOST
  else:
    seasonal_demand_boost = MONSOON_SEASON_BOOST
  
  holiday_demand_boost = 0
  if holiday:
    holiday_demand_boost = HOLIDAY_BOOST
  else:
    holiday_demand_boost = 0
  
  weekend_demand_boost = 0
  if weekend:
    weekend_demand_boost = WEEKEND_BOOST
  else:
    weekend_demand_boost = 0
  
  event_demand_boost = 0
  if nearby_event:
    event_demand_boost = EVENT_BOOST
  else:
    event_demand_boost = 0
  
  final_demand_unclipped = (base_demand + seasonal_demand_boost + holiday_demand_boost + weekend_demand_boost + event_demand_boost) 
  final_demand_clipped = (final_demand_unclipped/500) + random.uniform(-DEMAND_NOISE,DEMAND_NOISE)
  final_demand = round(final_demand_clipped,2)
  final_demand = max(0, min(final_demand, 1))

  # Calculate price
  demand_price_boost = final_demand * DEMAND_PRICE_FACTOR
  
  trend_price_boost = market_trend * MARKET_TREND_PRICE_FACTOR
  
  final_price = base_price + demand_price_boost + trend_price_boost + random.randint(-PRICE_NOISE,PRICE_NOISE) 
  
  final_price = round(final_price,2)
  
  competitor_price = final_price * (1 + property_features['competitor_bias']) + random.randint(-COMPETITOR_NOISE, COMPETITOR_NOISE)
  
  # Calculate occupancy
  occupancy_price_penalty = PRICE_ELASTICITY_FACTOR * ((final_price - competitor_price)/competitor_price)
  quality_occupancy_boost = QUALITY_BOOST_FACTOR * ((amenities_score + location_score)/20)
  occupancy = final_demand - occupancy_price_penalty + quality_occupancy_boost
  occupancy = round(1/(1 + exp(-occupancy)),2)
  
  revenue = final_price * occupancy
  return {
  'property_id': property_id,
  'date': date,
  'property_type': property_type,
  'location_score': location_score,
  'amenities_score': amenities_score,
  'rating': rating,
  'base_price': base_price,
  'month': month,
  'weekday': weekday,
  'weekend': weekend,
  'season': season,
  'holiday': holiday,
  'demand': final_demand,
  'competitor_price': competitor_price,
  'nearby_event': nearby_event,
  'market_trend': market_trend,
  'final_price': final_price,
  'occupancy_rate': occupancy,
  'revenue': revenue
  }
  
def generate_dataset() -> pd.DataFrame:
  """
  Generates a complete dataset with 500 date records for 500 properties each
  """
  
  dates = generateTemporalFeatures(base_market_trend=BASE_MARKET_TREND,market_trend_factor=MARKET_TREND_FACTOR,market_noise=MARKET_NOISE)
  dates = dates[:NUM_DATES]

  num_holidays = 0
  for i in dates:
    if i['holiday'] == 1:
      num_holidays+=1

  complete_dataset = []
  index = 0
  last_price = 0
  for i in range(NUM_PROPERTIES):
    property = generatePropertyFeatures(base_property_pricings=BASE_PROPERTY_PRICINGS,rating_price_factor=RATING_PRICE_FACTOR,competitor_bias_const=COMPETITOR_BIAS)
    for j in range(NUM_DATES):
      complete_dataset.append(processTemporalAndPropertyFeatures(i,property,dates[j]))
      last_price = complete_dataset[index]['final_price']
      index+=1

  complete_dataset_df = pd.DataFrame(complete_dataset)
  complete_dataset_df.to_csv("./datasets/raw/dataset.csv",index=False)
  return complete_dataset_df