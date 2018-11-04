'''

source activate py36

'''

def train_mod(saveModel=True, logging=True):

    import pandas as pd
    from create_model import create_mod
    import keras

    model, X, Y = create_mod()

    if logging:
        # Create a TensorBoard logger
        logger = keras.callbacks.TensorBoard(
            log_dir='logs',
            write_graph=True,    # log the structure of model to help visualizing the NN
            histogram_freq=5.    # write statsitcs on how each layers is working every 5 passes
        )

        # Train the model
        model.fit(
            X,
            Y,      # expected output
            epochs=50,    # training passes
            shuffle=True,
            verbose=2,
            callbacks=[logger]
        )
    else:
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

    if saveModel:
        model.save("trained_model.h5")
        print("Model saved to disk.")

    return model


if __name__ == '__main__':
    train_mod()