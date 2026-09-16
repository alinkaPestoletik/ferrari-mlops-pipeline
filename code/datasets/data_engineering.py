import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os


def load_data(base_path="data/raw"):
    results = pd.read_csv(f'{base_path}/results.csv')
    races = pd.read_csv(f'{base_path}/races.csv')
    constructors = pd.read_csv(f'{base_path}/constructors.csv')
    drivers = pd.read_csv(f'{base_path}/drivers.csv')
    return results, races, constructors, drivers


def clean_and_merge(results, races, constructors, drivers):
    ferrari_id = constructors[constructors['constructorRef'] == 'ferrari']['constructorId'].values[0]
    ferrari_results = results[results['constructorId'] == ferrari_id].copy()

    data = ferrari_results.merge(races, on='raceId', suffixes=('', '_race'))
    data = data.merge(drivers, on='driverId', suffixes=('', '_driver'))

    data = data.replace(r'\\N', np.nan, regex=True)
    data['target'] = (data['positionOrder'] <= 3).astype(int)

    features = ['grid', 'laps', 'year', 'driverRef']
    data[['grid', 'laps', 'year']] = data[['grid', 'laps', 'year']].apply(pd.to_numeric, errors='coerce')

    data = data.dropna(subset=features)
    data = data[(data['grid'] > 0) & (data['grid'] <= 30)]

    return data[features + ['target']]


def split_and_save(data, output_path="data/processed"):
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)

    os.makedirs(output_path, exist_ok=True)
    train_data.to_csv(f'{output_path}/train.csv', index=False)
    test_data.to_csv(f'{output_path}/test.csv', index=False)


if __name__ == "__main__":
    res, rac, cons, drv = load_data()
    cleaned_data = clean_and_merge(res, rac, cons, drv)
    split_and_save(cleaned_data)