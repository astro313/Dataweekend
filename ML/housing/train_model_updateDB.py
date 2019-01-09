'''

retrain model on updated data.

In reality, always check new model's accuracy/perfomance (compare to old) before using it.

'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


df = pd.read_csv("ml_house_data_set_updated.csv")

# Remove the unrelated fields from data
del df['house_number']
del df['unit_number']
del df['street_name']
del df['zip_code']

# Replace categorical data w/ one-hot encoded data
features_df = pd.get_dummies(df, columns=['garage_type', 'city'])

# Remove the sale price from the feature data
del features_df['sale_price']

# Create the X and y arrays
X = features_df.as_matrix()
y = df['sale_price'].as_matrix()

# shuffle and Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Fit regression model == value prediction
model = ensemble.GradientBoostingRegressor(
    n_estimators=1000,     # num of decision trees
    learning_rate=0.1,     # how much each individual decision tree influence the overall decision tree
    max_depth=6,           # each decision tree can be 6 layer deep
    min_samples_leaf=9,    # how many times a value must appear in training set for deicions tree to make a desicion base on it. At least 9 houses must exhibit the same characteristic before we consider it meaningful enough to build a deicison tree around it. Avoid single outliers to influence model too much.
    max_features=0.1,      # % of features in model randomly choose to consider each time we create a branch in decision tree
    loss='huber',
    random_state=0
)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'trained_house_classifier_model.pkl')

mse = mean_absolute_error(y_train, model.predict(X_train))
print("Training Set Mean Absolute Error: %.4f" % mse)

mse = mean_absolute_error(y_test, model.predict(X_test))
print("Test Set Mean Absolute Error: %.4f" % mse)

