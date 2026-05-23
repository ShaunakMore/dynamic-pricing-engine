import joblib
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

def evaluate_model(test_dataset,model_save_path="../models/lightgbm_dynamic_pricing.pkl"):
  model = joblib.load(model_save_path)

  test_dataset['date'] = pd.to_datetime(test_dataset['date'])

  test_valid_idx = test_dataset.dropna().index
  test_dataset = test_dataset.loc[test_valid_idx]

  X_test = test_dataset.drop(
    columns=[
      'revenue',
      'occupancy_rate',
      'property_id',
      'date'
    ]
  )
  y_test = test_dataset['occupancy_rate']

  X_test.columns = (
      X_test.columns
      .str.replace(' ', '_')
      .str.replace(r'[^A-Za-z0-9_]', '', regex=True)
  )

  y_pred = np.array(model.predict(X_test))

  mae = mean_absolute_error(y_true=y_test,y_pred=y_pred)
  mse = mean_squared_error(y_true=y_test,y_pred=y_pred)
  r2_scr = r2_score(y_true=y_test,y_pred=y_pred)

  print(f"Mean Aboslute Error: {mae}")
  print(f"Mean Squared Error: {mse}")
  print(f"R2 Score: {r2_scr}")