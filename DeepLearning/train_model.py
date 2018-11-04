'''

source activate py36

'''

def train_mod():

    import pandas as pd
    from create_model import create_mod

    model, X, Y = create_mod()

    # Train the model
    model.fit(
        X,
        Y,      # expected output
        epochs=50,    # training passes
        shuffle=True,
        verbose=2
    )

    test_data_df = pd.read_csv("sales_data_test_scaled.csv")
    X_test = test_data_df.drop('total_earnings', axis=1).values
    Y_test = test_data_df[['total_earnings']].values

    # calculate MSE
    test_error_rate = model.evaluate(X_test, Y_test, verbose=0)
    print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))
    return model