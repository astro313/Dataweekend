"""

Transfer learning: Keep all the layers that detect patterns in a pre-trained NN model, but remove the part that maps those patterns to specific obj. (the last dense layer). --> call this pre-trained NN "a feature extractor" because we are using it to extract training features from images.

Then create a new NN to replace the last layer in the original network.

Always try transfer learning first - quick and very useful when don't have lot of training data but already have a model that solves a similar problem.

Here, use TL to build an image recognition system that can identify pic of dogs. Need some training data (of dogs).

"""


from pathlib import Path
import numpy as np
import joblib
from keras.preprocessing import image
from keras.applications import vgg16

# use pretrained model to extract features from training images and save those features to a file.
# Path to folders with training data
dog_path = Path("training_data") / "dogs"
not_dog_path = Path("training_data") / "not_dogs"

images = []
labels = []

# Load not-dog
for img in not_dog_path.glob("*.png"):
    img = image.load_img(img)
    image_array = image.img_to_array(img)
    images.append(image_array)
    # For each 'not dog' image, the expected value of the label should be 0
    labels.append(0)

# load dog
for img in dog_path.glob("*.png"):
    img = image.load_img(img)
    image_array = image.img_to_array(img)
    images.append(image_array)
    # expected value should be 1
    labels.append(1)

# all the training images we load
x_train = np.array(images)
# convert labels to array
y_train = np.array(labels)

# use vgg16 model pretrained on the image net dataset.
# Normalize image data
x_train = vgg16.preprocess_input(x_train)

# Load a pre-trained NN (on imagenet) to use as a feature extractor
# so, chop off the last layer w/ include_top
pretrained_nn = vgg16.VGG16(weights='imagenet', include_top=False, \
                            input_shape=(64, 64, 3))

# Extract features for each image
features_x = pretrained_nn.predict(x_train)
# Save extracted features to file
joblib.dump(features_x, "x_train.dat")
# Save the matching array of expected values to a file
joblib.dump(y_train, "y_train.dat")
