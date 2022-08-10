import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import matplotlib

matplotlib.rcParams["figure.figsize"] = (20 , 10)


#read the data and return a csv file

def read_data():
    df1 = pd.read_csv("Bengaluru_House_Data.csv")

    # drop
    df2 = df1.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')

    return df2



df2 = read_data()


df3 = df2.dropna()


#remove bhk , bedroom and any string from bedroom column
df3['bhk'] = df3['size'].apply(lambda x: int(x.split(" ")[0]))
# print(df3.head())

# print(df3['bhk'].unique())

# print(df3[df3.bhk>20])

#Check
print(df3.total_sqft.unique())


def is_float(x):
    try:
        float(x)
        return True
    except:
        return False


#returns values that are not floats.




def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens)==2:
        #return the average
        return (float(tokens[0]) + float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None

#Find total_sqft data which is not float
print(df3[~df3['total_sqft'].apply(is_float)])

#Convert to sq.ft
df4 = df3.copy()
df4['total_sqft'] = (df4['total_sqft'].apply(convert_sqft_to_num))
#if 1350-52 gets average ,
#if 340 sq.ft gets nothing



#Create price_per_sqft_columns
df5 = df4.copy()
df5['price_per_sqft'] = df5['price']*100000/df5['total_sqft']

#See unique locations
# See dimensionality reduction

print(len(df5.location.unique()))



def dimensionality_reduction(df5):
    df5.location = df5.location.apply(lambda x: x.strip())
    # See locations with many datapoints.
    location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
    print("Number of unique locations")
    print(location_stats)

    location_stats_less_than_10 = location_stats[location_stats <= 10]

    df5.location = df5.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

    return df5



df5 = dimensionality_reduction(df5)





print(len(df5.location.unique()))

#Only keep those values for which the sq.ft by bedroom is more than 300
df6 = df5[~(df5.total_sqft/df5.bhk<300)]

print(df6.shape)
def outlier_detection(df):
    # REMOVE EXTREME VARIANCE


    df_out = pd.DataFrame()
    for key , subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df=subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out , reduced_df] , ignore_index=True)

    return df_out

df7 = outlier_detection(df6)

#Removed 2000 shapes.
print(df7.shape )

# For each location , if there are 2bhk bedrooms which are higher than 3bhk bedrooms for similar sqft area , remove those


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
df8 = remove_bhk_outliers(df7)

print(df8.shape)

#Remove bathroom_outliers

df9 = df8[df8.bath<df8.bhk+2]
print(df9.shape)

#drop features that are not needed .

df10 = df9.drop(['size','price_per_sqft'],axis='columns')
print(df10.head(3))


#One hot encode the data
dummies = pd.get_dummies(df10.location)


#Append the dataframe to to our pre-processed dataframe
#Need to drop one of the dummy variable
df11 = pd.concat([df10,dummies.drop('other',axis='columns')],axis='columns')

print(df11.head(2))
#Drop the location variable
df12 = df11.drop('location',axis='columns')
df12.head(2)

