'''Contains the utility files , it loads the model , the required locations and saves it'''


'''Format for prediction
location , bath , sqft , bhk'''

import json
import pickle
import numpy as np


#Declare global variables
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location , bath , sqft , bhk):
    ''' First prepares the data so that it is acceptable by the linear_classification_function . Because we are using one
    hot encoding , we need to find where the location is located in our csv file.'''
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    #Create np array
    x = np.zeros(len(__data_columns))
    print("The number of columns %d" , len(__data_columns))

    x[0] = bath
    x[1] = sqft
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1
    return  round(__model.predict([x])[0] , 2)


def get_locations():
    ''' From the columns.json file , it gets the location name of each location(zipcode) in our csv file'''
    load_artifacts()
    return (__locations)


def load_artifacts():
    '''Loads our machine learning model '''

    print("Loading the artifacts")
    global __data_columns
    global __locations
    global __model


    # read the file
    with open('Artifacts/location_columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        print("I OPENED THE JSON FILE")
        # starting with column number 3 you can get the values.
        __locations = __data_columns[4:]

    with open('Artifacts/redfin_price_model.pickle', 'rb') as f:
        __model = pickle.load(f)

    print('Artifacts are loaded')


if __name__ == '__main__':
    load_artifacts()
    print(get_locations())
    print(get_estimated_price('mesquite TX 75150' ,  3 , 2040 , 4))
    print(get_estimated_price('Other' , 2 , 2040 , 4))
    print(get_estimated_price('Carrollton TX 75007' ,  3 , 2040 , 4))


