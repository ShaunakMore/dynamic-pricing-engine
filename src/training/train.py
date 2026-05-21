from lightgbm import LGBMRegressor
import pandas as pd
import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import joblib

def train_model(train_dataset: pd.DataFrame, test_dataset: pd.DataFrame):

  train_dataset['date'] = pd.to_datetime(train_dataset['date'])
  test_dataset['date'] = pd.to_datetime(test_dataset['date'])

  train_valid_idx = train_dataset.dropna().index

  train_dataset = train_dataset.loc[train_valid_idx]

  test_valid_idx = test_dataset.dropna().index

  test_dataset = test_dataset.loc[test_valid_idx]

  X_train = train_dataset.drop(
    columns=[
      'property_id',
      'date',
      'revenue',
      'occupancy_rate',
      'Unnamed: 1'
    ]
  )

  y_train = train_dataset['occupancy_rate']

  X_test = test_dataset.drop(
    columns=[
      'property_id',
      'date',
      'revenue',
      'occupancy_rate',
      'Unnamed: 1'
    ]
  )

  y_test = test_dataset['occupancy_rate']

  X_train.columns = (
      X_train.columns
      .str.replace(' ', '_')
      .str.replace(r'[^A-Za-z0-9_]', '', regex=True)
  )

  X_test.columns = (
      X_test.columns
      .str.replace(' ', '_')
      .str.replace(r'[^A-Za-z0-9_]', '', regex=True)
  )

  train_valid_idx = X_train.dropna().index

  X_train = X_train.loc[train_valid_idx]
  y_train = y_train.loc[train_valid_idx]

  test_valid_idx = X_test.dropna().index

  X_test = X_test.loc[test_valid_idx]
  y_test = y_test.loc[test_valid_idx]

  model = LGBMRegressor()
  model.fit(X_train,y_train)

  preds = np.array(model.predict(X_test))


  mae = mean_absolute_error(y_true=y_test,y_pred=preds)
  mse = mean_squared_error(y_true=y_test,y_pred=preds)
  r2_scr = r2_score(y_true=y_test,y_pred=preds)

  print(f"Mean Aboslute Error: {mae}")
  print(f"Mean Squared Error: {mse}")
  print(f"R2 Score: {r2_scr}")

  joblib.dump(
    model,
    "../models/lightgbm_dynamic_pricing.pkl"
  )