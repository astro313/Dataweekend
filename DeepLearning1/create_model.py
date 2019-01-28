'''

source activate py36

'''

import pandas as pd
from keras.models import Sequential
from keras.layers import *


def create_mod():
    training_data_df = pd.read_csv("sales_data_training_scaled.csv")

    X = training_data_df.drop('total_earnings', axis=1).values    # split off feature
    Y = training_data_df[['total_earnings']].values

    # Define the model
    model = Sequential()
    model.add(Dense(50, input_dim=9, activation='relu', name='layer_1'))   # 50 nodes, first layer need input_dim = # of features; densely connected: each node connected to each other node in another layer
    model.add(Dense(100, activation='relu', name='layer_2'))
    model.add(Dense(50, activation='relu', name='layer_3'))
    model.add(Dense(1, activation='linear', name='output_layer'))         # finally, 1 node for prediction. Linear since it's a single linear value
    model.compile(loss="mean_squared_error", optimizer="adam")
    return model, X, Y