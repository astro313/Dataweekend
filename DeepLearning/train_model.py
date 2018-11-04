'''

source activate py36

'''

def train_mod(runName, saveModel=True, exportModel=True, logging=False):

    import pandas as pd
    from create_model import create_mod
    import keras

    model, X, Y = create_mod()

    test_data_df = pd.read_csv("sales_data_test_scaled.csv")
    X_test = test_data_df.drop('total_earnings', axis=1).values
    Y_test = test_data_df[['total_earnings']].values

    if logging:
        # Create a TensorBoard logger
        logger = keras.callbacks.TensorBoard(
            log_dir='logs/{}'.format(runName),
            write_graph=True,    # log the structure of model to help visualizing the NN
#            histogram_freq=5.    # write statsitcs on how each layers is working every 5 passes
        )

        # Train the model
        model.fit(
            X,
            Y,      # expected output
            epochs=50,    # training passes
            shuffle=True,
            verbose=2,
            callbacks=[logger],
#             validation_data=(X_test, Y_test)
        )

        import webbrowser, os

        # to prevent cannot bind to port 6006:
        os.system("lsof -i:6006")
        print("Kill leftover process to prevent cannot bind to port 6006")

        os.system('tensorboard --logdir=logs')
        webbrowser.open("http://localhost:6006")

    else:
        # Train the model
        model.fit(
            X,
            Y,      # expected output
            epochs=50,    # training passes
            shuffle=True,
            verbose=2
        )

    # calculate MSE
    test_error_rate = model.evaluate(X_test, Y_test, verbose=0)
    print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))

    if saveModel:  # on disk
        model.save("trained_model.h5")
        print("Model saved to disk.")

    if exportModel:
        ''' scale up in production for large number of users '''

        import tensorflow as tf
        from keras import backend as K

        model_builder = tf.saved_model.builder.SavedModelBuilder("exported_model")

        inputs = {
            'input': tf.saved_model.utils.build_tensor_info(model.input)
        }
        outputs = {
            'earnings': tf.saved_model.utils.build_tensor_info(model.output)
        }

        # like func declaration
        signature_def = tf.saved_model.signature_def_utils.build_signature_def(
            inputs=inputs,
            outputs=outputs,
            method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
        )

        model_builder.add_meta_graph_and_variables(
            K.get_session(),
            tags=[tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature_def
            }
        )

        model_builder.save()


    return model


if __name__ == '__main__':
    runName = "run 1 with 50 nodes"
    train_mod(runName=runName)