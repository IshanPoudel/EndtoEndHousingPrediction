import json
import pickle
from util import get_locations
from util import load_artifacts
from util import get_estimated_price


from flask import Flask , request , jsonify

app = Flask(__name__)



@app.route('/hello')
def hello():
    return "Hi"


@app.route('/get_location_name' , methods=['POST'])
def prediction():

    locations = get_locations()
    #Create response to send
    response = jsonify({
        'locations' : locations
    })

    response.headers.add('Access-Control-Allow-Origin' , '*')

    return response



@app.route('/get_prediction' , methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = float(request.form['location'])
    bhk = float(request.form['bhk'])
    bath = float(request.form['bath'])

    response = jsonify({
        'estimated_price' : get_estimated_price(location , bath , total_sqft , bhk)

    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response




if __name__ == '__main__':
    print("Starting python server for housing price prediction")
    app.run()


