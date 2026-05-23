import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor

def predict_prices_batch(model: LGBMRegressor, test_dataset: pd.DataFrame, max_price_steps = 200):
    N = len(test_dataset)  
    M = max_price_steps
    
    df_expanded = test_dataset.loc[test_dataset.index.repeat(M)].copy()
    
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