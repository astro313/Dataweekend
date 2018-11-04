'''

Rescale each col of data to a small range like 0 to 1 (all col needs to be in comparable range for NN training to work well).

'''

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

training_data_df = pd.read_csv("sales_data_training.csv")
test_data_df = pd.read_csv("sales_data_test.csv")

scaler = MinMaxScaler(feature_range=(0, 1))

scaled_training = scaler.fit_transform(training_data_df)   # first fit a scalar then transform
scaled_testing = scaler.transform(test_data_df)            # scale test set the same way

# Print the scaler applied to total_earnings
print("Note: total_earnings values were scaled by multiplying by {:.10f} and adding {:.6f}".format(scaler.scale_[8], scaler.min_[8]))
# Note: total_earnings values were scaled by multiplying by 0.0000036968 and adding -0.115913

# pd obj from scaled data so we can save to csv
scaled_training_df = pd.DataFrame(scaled_training,
                                  columns=training_data_df.columns.values)
scaled_testing_df = pd.DataFrame(scaled_testing,
                                 columns=test_data_df.columns.values)

scaled_training_df.to_csv("sales_data_training_scaled.csv", index=False)
scaled_testing_df.to_csv("sales_data_testing_scaled.csv", index=False)