import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

def load_data(fname: str):
    data = pd.DataFram(pd.read_csv(fname), index=None)
    print(f'Data Shape: {data.shape}')
    return data

def split_input_output(data, target_col):
    X = data.drop(columns=target_col)
    y = data[target_col]
    
    print(f"Original data shape: {data.shape}")
    print(f"X data shape: {X.shape}")
    print(f"y data shape: {y.shape}")
    
    return X, y

def split_train_test(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    print(f'X_train shape: {X_train.shape}')
    print(f'X_test shape: {X_test.shape}')
    print(f'y_train shape: {y_train.shape}')
    print(f'y_test shape: {y_test.shape}')
    return X_train, X_test, y_train, y_test

def serialize_data(data, path):
    joblib.dump(data, path)
    print(f'Data serialized to {path}')

def deserialize_data(path):
    data = joblib.load(path)
    print(f'Data deserialized from {path}')
    return data

