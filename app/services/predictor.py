import joblib
import pandas as pd
import numpy as np
from app.schemas.request_schemas import OccupancyPredictionRequest

model = joblib.load("./models/occupancy_model.pkl")

BASE_PROPERTY_PRICINGS = { 
              "Entire house": 3000,
              "Private room": 1000,
              "Luxury suite": 2000
              }

def predict_occupancy_rate(features:OccupancyPredictionRequest):
  
  model_column_order = [ "location_score","amenities_score","rating",
                        "base_price","month","weekend",
                        "holiday","demand","competitor_price",
                        "nearby_event", "market_trend", "final_price",
                        "season_Monsoon", "season_Summer", "season_Winter", 
                        "weekday_Friday","weekday_Monday","weekday_Saturday",
                        "weekday_Sunday","weekday_Thursday","weekday_Tuesday",
                        "weekday_Wednesday", "property_type_Entire_house",
                        "property_type_Luxury_suite","property_type_Private_room"]
  
  all_seasons = ["Summer","Winter","Monsoon"]
  all_property_types = [ "Entire house","Private room","Luxury suite"]
  all_weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
  base_price = BASE_PROPERTY_PRICINGS[features.property_type]
  
  curr_date = pd.Timestamp.now()
  month = curr_date.month
  
  season = ""
  if 3 <= month <= 6:
    season = "Summer"
  
  elif 7 <= month <= 9:
    season ="Monsoon"
  
  else:
    season = "Winter"
  
  prediction_df = pd.DataFrame({
    "base_price":base_price,
    "month": month,
    "weekend": 1 if curr_date.day_of_week == 5 or curr_date.day_of_week == 6 else 0,
    "weekday":curr_date.day_name(), 
    "location_score": [features.location_score],
    "amenities_score":[features.amenitites_score],
    "rating": [features.rating],
    "demand": [features.demand],
    "competitor_price": [features.competitor_price],
    "market_trend": [features.market_trend],
    "final_price": [features.final_price],
    "season": season,
    "property_type":features.property_type,
    "nearby_event":features.nearby_event,
    "holiday": features.holiday
  })
  
  prediction_df['season'] = pd.Categorical(prediction_df['season'],categories=all_seasons)
  prediction_df = pd.get_dummies(prediction_df,columns=['season'],dtype=int)
  
  prediction_df['property_type'] = pd.Categorical(prediction_df['property_type'],categories=all_property_types)
  prediction_df = pd.get_dummies(prediction_df,columns=['property_type'],dtype=int)
  
  prediction_df['weekday'] = pd.Categorical(prediction_df['weekday'],categories=all_weekdays)
  prediction_df = pd.get_dummies(prediction_df,columns=['weekday'],dtype=int)
  
  prediction_df.columns = (
    prediction_df.columns
    .str.replace(' ', '_')
    .str.replace(r'[^A-Za-z0-9_]', '', regex=True)
)
  prediction_df = prediction_df[model_column_order]
  
  print(f"Prediction df: {prediction_df}")
  return model.predict(prediction_df)[0],prediction_df

def optimize_pricing(prediction_df: pd.DataFrame,max_price_steps = 200):
    N = len(prediction_df)  
    M = max_price_steps
    
    df_expanded = prediction_df.loc[prediction_df.index.repeat(M)].copy()
    
    price_increments = np.tile(np.arange(M) * 5, N)
    df_expanded['final_price'] = df_expanded['base_price'] + price_increments
    
    predicted_occupancies = model.predict(df_expanded)
    
    prices_matrix = df_expanded['final_price'].values.reshape(N, M)
    occupancy_matrix = predicted_occupancies.reshape(N, M)
    
    revenue_matrix = prices_matrix * occupancy_matrix
    
    best_indices = np.argmax(revenue_matrix, axis=1)
    best_prices = prices_matrix[np.arange(N), best_indices]
    
    max_revenues = np.max(revenue_matrix, axis=1)
    
    return best_prices.tolist(), max_revenues.tolist()