"""

Transfer learning.

Use the pre-trained NN to extract features from training images. Then train a new NN that uses those extracted features.

"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from pathlib import Path
import joblib

# Load data set (extracted features) from feature extraction
x_train = joblib.load("x_train.dat")
y_train = joblib.load("y_train.dat")

# since we use vgg16 to extract features from image, this NN has no convolutional layers. Instead, it only has the final dense layer of the NN.
# Create a model and add layers
model = Sequential()

model.add(Flatten(input_shape=x_train.shape[1:]))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=['accuracy']
)

# Train the model
model.fit(
    x_train,
    y_train,
    epochs=10,
    shuffle=True
)

# Save NN structure and trained weights
model_structure = model.to_json()
f = Path("model_structure.json")
f.write_text(model_structure)
model.save_weights("model_weights.h5")
