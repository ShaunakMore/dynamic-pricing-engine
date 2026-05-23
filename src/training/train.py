from lightgbm import LGBMRegressor
import pandas as pd
import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
import joblib
import mlflow
from mlflow.lightgbm import log_model as lgbm_log_model

def train_model(train_dataset: pd.DataFrame, test_dataset: pd.DataFrame,model_save_path="./models/occupancy_model.pkl"):

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
    ]
  )

  y_train = train_dataset['occupancy_rate']

  X_test = test_dataset.drop(
    columns=[
      'property_id',
      'date',
      'revenue',
      'occupancy_rate',
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

  mlflow.set_experiment("price-prediction")
  with mlflow.start_run():
    mlflow.set_tags({
      "train_size": len(X_train),
      "test_size": len(X_test),
      "n_features": X_train.shape[1],
    })
    model = LGBMRegressor()
    
    mlflow.log_params(model.get_params())
    
    model.fit(X_train,y_train)
    
    preds = np.array(model.predict(X_test))


    mae = mean_absolute_error(y_true=y_test,y_pred=preds)
    mse = mean_squared_error(y_true=y_test,y_pred=preds)
    r2_scr = r2_score(y_true=y_test,y_pred=preds)

    mlflow.log_metric(
      "mae", 
      mae
    )
    mlflow.log_metric(
      "mse",
      mse
    )
    mlflow.log_metric(
      "r2score",
      r2_scr
    )
    
    importance_df = pd.DataFrame({
      "features": model.feature_name_,
      "importance_gain": model.booster_.feature_importance(importance_type="gain"),
      "importance_split":model.booster_.feature_importance(importance_type="split")
    }).sort_values("importance_gain",ascending=False)
    importance_df.to_csv("./datasets/processed/feature_importance.csv",index=False)
    mlflow.log_artifact("./datasets/processed/feature_importance.csv")
    
    print(f"Mean Aboslute Error: {mae}")
    print(f"Mean Squared Error: {mse}")
    print(f"R2 Score: {r2_scr}")

    joblib.dump(
      model,
      model_save_path
    )
    
    lgbm_log_model(
      model,
      name="lightgbm_model"
    )
    