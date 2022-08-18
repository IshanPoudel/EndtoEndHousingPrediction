''' Given the location , it creates a housing model and saves it. '''

# location = ['North Dallas']
# from PreprocessingPipeline import get_final_data_frame
from PreprocessingPipeline import get_final_data_frame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score
import pickle


def predict_price(location, sqft, bath, bhk):
    index_for_location = np.where(X.columns == location)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = bath
    x[1] = sqft
    x[2] = bhk
    if index_for_location >= 0:
        x[index_for_location] = 1

    return linear_classification.predict([x])[0]



def create():

    global X

    final_df = get_final_data_frame()
    #export dataframe to csv
    # final_df.to_csv('file_name.csv’)
    final_df.to_csv('Check.csv')
    X = final_df.drop('price', axis='columns')

    print(X.head())
    y = final_df.price

    # Create model.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    global linear_classification

    linear_classification = LinearRegression()
    linear_classification.fit(X_train, y_train)
    print("Accuracy")
    print(linear_classification.score(X_test.values, y_test))



    # Shuffle_Split will equally disrtribute the dataset
    cross_validation_metric = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

    print("Accuracy across iterations")
    print(cross_val_score(LinearRegression(), X, y, cv=cross_validation_metric))





    #Store the model

    with open('server/Artifacts/redfin_price_model.pickle', 'wb') as f:
        pickle.dump(linear_classification, f)


    #Find a way to store the columns
    import json

    columns = {
        'data_columns' : [col.lower() for col in X.columns]
    }
    with open('server/Artifacts/location_columns.json', 'w') as f:
        f.write(json.dumps(columns))



    print(predict_price('Carrollton TX 75007' ,  2040 , 2,  4))


create()