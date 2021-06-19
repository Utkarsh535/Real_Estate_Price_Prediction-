import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[4:]  # first 4 columns are sqft, bath, bhk , balcony

    global __model
    if __model is None:
        with open('./artifacts/banglore_home_price_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

def get_estimated_price(location, total_sqft, size_in_bhk, bath,balcony):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    X = np.zeros(len(__data_columns))
    X[0] = total_sqft
    X[1] = bath
    X[2] = size_in_bhk
    X[3] = balcony
    # x[0][3] = balcony
    if loc_index >= 0:
        X[loc_index] = 1

    # price = __model.predict([X])[0]
    return round(__model.predict([X])[0],2)
    # return round(float(price),2)
if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3,2))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2,2,2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2,2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2,4,2))  # other location
