import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import matplotlib

matplotlib.rcParams["figure.figsize"] = (20 , 10)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
#read the data and return a csv file


def read_data():
    df1 = pd.read_csv("Bengaluru_House_Data.csv")

    # drop
    df2 = df1.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')

    return df2

def is_float(x):
    try:
        float(x)
        return True
    except:
        return False

def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens)==2:
        #return the average
        return (float(tokens[0]) + float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None


def dimensionality_reduction(df5):

    #If there are less than 10 location datapoints group them into other column.
    df5.location = df5.location.apply(lambda x: x.strip())
    # See locations with many datapoints.
    location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
    # print("Number of unique locations")
    # print(location_stats)

    location_stats_less_than_10 = location_stats[location_stats <= 10]

    #if location in location_stats_less_than_10 put the location as other.
    df5.location = df5.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

    return df5

def outlier_detection(df):
    # REMOVE EXTREME VARIANCE
    # if price_per_sq_ft is extreme for any houses in a location , take them off

    df_out = pd.DataFrame()
    for key , subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df=subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out , reduced_df] , ignore_index=True)

    return df_out

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')

def preprocess(df2):
    #Drop empty columns
    df3 = df2.dropna()

    # remove bhk , bedroom and any string from bedroom column
    df3['bhk'] = df3['size'].apply(lambda x: int(x.split(" ")[0]))

    df4 = df3.copy()

    #if sq.ft numbers are not just variables.
    df4['total_sqft'] = (df4['total_sqft'].apply(convert_sqft_to_num))

    #Create price_per_sqft column for outlier detection
    df5 = df4.copy()
    df5['price_per_sqft'] = df5['price'] * 100000 / df5['total_sqft']

    df5 = dimensionality_reduction(df5)

    # Only keep those values for which the sq.ft by bedroom is more than 300
    df6 = df5[~(df5.total_sqft / df5.bhk < 300)]

    df7 = outlier_detection(df6)

    # For each location , if there are 2bhk bedrooms which are higher than 3bhk bedrooms for similar sqft area , remove those
    df8 = remove_bhk_outliers(df7)

    # Remove bathroom_outliers

    df9 = df8[df8.bath < df8.bhk + 2]
    print(df9.shape)

    # drop features that are not needed .

    df10 = df9.drop(['size', 'price_per_sqft'], axis='columns')
    print(df10.head(3))

    # One hot encode the data
    dummies = pd.get_dummies(df10.location)

    # Append the dataframe to to our pre-processed dataframe
    # Need to drop one of the dummy variable
    df11 = pd.concat([df10, dummies.drop('other', axis='columns')], axis='columns')

    print(df11.head(2))
    # Drop the location variable
    df12 = df11.drop('location', axis='columns')
    df12.head(2)

    return df12


df2 = read_data()
final_df = preprocess(df2)
print(final_df.shape)

X = final_df.drop('price' , axis = 'columns')
X.head()
y = final_df.price

#Create model.
X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.2 , random_state=10)


linear_classification  = LinearRegression()
linear_classification.fit(X_train , y_train)
print("Accuracy")
print(linear_classification.score(X_test , y_test))


from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

#Shuffle_Split will equally disrtribute the dataset
cross_validation_metric = ShuffleSplit(n_splits=5 , test_size=0.2 , random_state=0)

print("Accuracy across iterations")
print(cross_val_score(LinearRegression() , X , y ,cv = cross_validation_metric ))














