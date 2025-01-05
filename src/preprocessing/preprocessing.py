import pickle
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

encoder_path = {
    'buying': '../../model/ohe_buying.pkl',
    'maint': '../../model/ohe_maint.pkl',
    'doors': '../../model/ohe_doors.pkl',
    'persons': '../../model/ohe_persons.pkl',
    'lug_boot': '../../model/ohe_lug_boot.pkl',
    'safety': '../../model/ohe_safety.pkl',
    'target': '../../model/le_target.pkl'
}

dataset_path = '../../data/processed/car.csv'
dataset_ready_path = '../../data/processed/car_dataset.pkl'

sep = '\t'
index_col = 'index'
list_columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'target']

column_categories = {
    'buying': np.array(['vhigh', 'high', 'med', 'low']).reshape(-1, 1),
    'maint': np.array(['vhigh', 'high', 'med', 'low']).reshape(-1, 1),
    'doors': np.array(['2', '3', '4', '5more']).reshape(-1, 1),
    'persons': np.array(['2', '4', 'more']).reshape(-1, 1),
    'lug_boot': np.array(['small', 'med', 'big']).reshape(-1, 1),
    'safety': np.array(['low', 'med', 'high']).reshape(-1, 1),
    'target': np.array(['unacc', 'acc', 'good', 'vgood']).reshape(-1, 1)
}

def load_data(fname: str):
    data = pd.read_csv(fname, sep='\t', index_col="index")
    print(f'Data Shape: {data.shape}')
    return data

def main():
    data = load_data(dataset_path)
    data.columns = list_columns
    data.index.name = None
    for column in data.columns:
        if (column != 'target'):
            ohe = OneHotEncoder(sparse_output=False)
            ohe.fit(column_categories[column])
            temp = pd.DataFrame(ohe.transform(data[[column]].to_numpy().reshape(-1,1)),
                                columns=[column + '_' + name for name in ohe.categories_[0].tolist()])
            data = pd.concat([data, temp], axis=1)
            data.drop(columns=column, inplace=True)
            joblib.dump(ohe, encoder_path[column])
            print(f"Column {column} has been encoded")
            print(f"Data has been serialized to {dataset_ready_path}")
        elif (column == 'target'):
            le = LabelEncoder()
            le.fit(column_categories[column].reshape(-1))
            data[column] = le.transform(data[column])
            joblib.dump(le, encoder_path[column])
            print(f"Column {column} has been encoded")
            print(f"Data has been serialized to {dataset_ready_path}")
    
    data.to_pickle(dataset_ready_path)
if __name__ == '__main__':
    main()