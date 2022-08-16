import json
import pickle

from flask import Flask , request , jsonify

app = Flask(__name__)



@app.route('/hello')
def hello():
    return "Hi"


def get_locations():
    ''' From the columns.json file , it gets the location name of each location(zipcode) in our csv file'''
    print("The locations are")
    print(__locations)


def load_artifacts():
    '''Loads our machine learning model '''

    print("Loading the artifacts")
    global __data_columns
    global __model


    #read the file
    with open('Artifacts/location_columns.json' , 'r') as f:
        __data_columns = json.load(f)['data_columns']
        #starting with column number 3 you can get the values.
        __locations = __data_columns[3:]

    with open('Artifacts/redfin_price_model.pickle' , 'rb') as f:
        __model = pickle.load(f)

    print('Artifacts are loaded')








if __name__ == '__main__':
    print("Starting python server for housing price prediction")
    app.run()


