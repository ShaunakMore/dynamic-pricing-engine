import pandas as pd
from pathlib import Path

def process_dataset(dataset:pd.DataFrame):
  """
  Process raw dataset and perform EDA operations and generate test and train datasets.
  """

  dataset['date'] = pd.to_datetime(dataset['date'])

  na_values = dataset.isna()
  print(f"Number of NA values: {len(na_values[na_values.eq(True).any(axis='columns')])}")

  null_values = dataset.isnull()
  print(f"Number of NULL values: {len(null_values[null_values.eq(True).any(axis='columns')])}")


  dataset = pd.get_dummies(
    dataset,
    columns=['season'],
    dtype=int
  )

  dataset = pd.get_dummies(
    dataset,
    columns=['weekday'],
    dtype=int
  )

  dataset = pd.get_dummies(
    dataset,
    columns=['property_type'],
    dtype=int
  )

  dataset['occupancy_lag_1'] = (
      dataset
      .groupby('property_id')['demand']
      .shift(1)
  )

  dataset['price_lag_1'] = (
    dataset
    .groupby('property_id')['final_price']
    .shift(1)
  )

  dataset['demand_lag_1'] = (
    dataset
    .groupby('property_id')['demand']
    .shift(1)
  )
  dataset = dataset.sort_values(
      ['property_id', 'date']
  )

  dataset['rolling_7_day_demand'] = (
      dataset
      .groupby('property_id')['demand']
      .transform(
          lambda x:
          x.rolling(7, min_periods=1).mean()
      )
  )

  dataset['rolling_30_day_price'] = (
      dataset
      .groupby('property_id')['final_price']
      .transform(
          lambda x:
            x.rolling(window=30,min_periods=1).mean() 
      )    
  )

  dataset.to_csv("./datasets/processed_dataset.csv",index=False)

  train_dataset = (
    dataset.groupby(['property_id']).apply(lambda x: x[:int(0.8 * len(x))])
  )

  test_dataset = (
    dataset.groupby('property_id').apply(lambda x: x[int(0.8 * len(x)):])
  )

  train_dataset.to_csv('./datasets/train_dataset.csv')
  test_dataset.to_csv('./datasets/test_dataset.csv')

  return train_dataset,test_dataset