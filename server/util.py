'''Contains the utility files , it loads the model , the required locations and saves it'''

import json
import pickle


#Declare global variables
__locations = None
__data_columns = None
__model = None

def get_locations():
    ''' From the columns.json file , it gets the location name of each location(zipcode) in our csv file'''
    print("The locations are")
    print(__locations)


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


load_artifacts()
get_locations()