import pandas as pd
from keras.models import load_model

model = load_model('trained_model.h5')
X = pd.read_csv("proposed_new_product.csv").values

# Make prediction
prediction = model.predict(X)[0][0]

# Re-scale the data from the 0-to-1 range back to dollars
# These constants are from when the data was originally scaled down to the 0-to-1 range, from preprocess_data.py
prediction = prediction + 0.1159
prediction = prediction / 0.0000036968

print("Earnings Prediction for Proposed Product - ${}".format(prediction))
