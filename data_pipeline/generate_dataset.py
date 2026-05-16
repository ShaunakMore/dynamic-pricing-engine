import datetime
import pandas as pd
import random
RANDOM_SEED = 42

def get_season(month:int) -> str:
  """
  Function to return the season (according to seasons in the Indian subcontinent) 
  based on month of the year
  """
  
  if 3 <= month <= 6:
    return "Summer"
  
  elif 7 <= month <= 9:
    return "Monsoon"
  
  else:
    return "Winter"
  
def generate_property_features() -> pd.DataFrame:
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
  
  final_norm_rating = (final_rating/300) * 5
      
  return pd.DataFrame({
    'room_type': [property_type],
    'rating': [round(final_norm_rating,2)],
    'amenities_score': [amenities_score],
    'location_score': [location_score]
  })

def generate_temporal_features() -> list[pd.DataFrame]:
  
  date_range = pd.date_range('2024-01-01','2025-12-31').to_list()

  temporal_data_frame = [pd.DataFrame({
    'date': [date.strftime('%Y-%m-%d')],
    'month': [date.month],
    'weekday': [date.day_name()],
    'weekend': [0 if date.weekday == 5 or date.weekday == 6 else 1],
    'season': [get_season(date.month)]
  }) for date in date_range]  
  
  return temporal_data_frame

temporal_data = generate_temporal_features()
print(f"Temporal data:\n{temporal_data[0]}")

property_features = generate_property_features()
print(f"Property Features:\n{property_features}")

