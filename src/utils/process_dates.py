import pandas as pd
import random
from src.utils.get_season import getSeason

def processDates(date: pd.Timestamp,BASE_MARKET_TREND,MARKET_TREND_FACTOR, MARKET_NOISE) -> dict:
  """
  Processes dates to extract additional features.
  """
  processed_date = date.strftime('%Y-%m-%d')
  month = date.month
  weekday = date.day_name()
  weekend = 1 if date.weekday() == 5 or date.weekday() == 6 else 0
  season = getSeason(date.month)
  holiday = 0 if random.randint(0,100) < 95 else 1
  nearby_event =  0 if random.randint(0,100) < 90 else 1
  market_trend = BASE_MARKET_TREND + ((date - pd.to_datetime('2024-01-01')).days * MARKET_TREND_FACTOR) + random.uniform(-MARKET_NOISE,MARKET_NOISE)

  return {
    'date': processed_date,
    'month': month,
    'weekday': weekday,
    'weekend': weekend,
    'season': season,
    'holiday': holiday,
    'nearby_event': nearby_event,
    'market_trend':market_trend
  }