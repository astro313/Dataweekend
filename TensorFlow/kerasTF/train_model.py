
'''

source activate py36

'''

import keras
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from pathlib import Path

# if I'm on rusty GPU
import socket, os
host = socket.gethostname()
if 'worker' in host:
    os.system('module load cuda cudnn')
    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    from keras import backend as K
    K.tensorflow_backend._get_available_gpus()
    os.system('nvidia-smi &')

# Load data
# image and labels
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize 0-255 pix val to 0-to-1
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# one-hot encoding
# Convert label (w/ single values from 0-9) to binary class matrices
# so that each label is array with on element set to 1 and and the rest set to 0.
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

# Create a model and add layers
model = Sequential()     # so we can add layers in sequential

# add CNN to better detect patterns from images
model.add(Conv2D(32, (3, 3),    # 32 filters - each capable of detecting one pattern in image; split image into 3x3 tiles.
            padding="same",     # pad zero so img w/ (32x32) for window size (3x3) can work out
            activation="relu",
            input_shape=(32, 32, 3)))
model.add(Conv2D(32, (3, 3), activation="relu"))    # no padding
model.add(MaxPooling2D(pool_size=(2, 2)))           # region size to pull tgt
model.add(Dropout(0.25))     # percent of NN coonections to randomly cut

model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))   # 64 filters
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# transition from 2D data to 1D
model.add(Flatten())
# then Dense layers
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.5))     # make NN work really hard
model.add(Dense(10, activation="softmax"))     # one node for each class, softmax ensure all 10 values adds up to 1 (as it should for likelihood)

# Compile model to memory
model.compile(
    loss='categorical_crossentropy',     # classify an image into different (>1) categories
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()
# Note total number of weights (params) in the model


# Train model
model.fit(
    x_train,
    y_train,
    batch_size=32,    # how many images to feed into network at once during training, typically 32-128
    epochs=30,        # how many pass through the entire training set
    validation_data=(x_test, y_test),    # used for testing accuracy, not use for training
    shuffle=True
)
# If loss doesn't go down, and accuracy doesn't go up over time, that means there's either sth wrong w/ the neural network design, or that there are problems w/ the training data.
# it's possible that dataset is too small to train the neural network, or that the neural network doesn't have enough layers to capture the patterns in the dataset.

# Save neural network structure
model_structure = model.to_json()
f = Path("model_structure.json")
f.write_text(model_structure)

# Save neural network's trained weights
model.save_weights("model_weights.h5")
