"""

Use transfer learning to create and train a NN that recognize pic of dogs.

Use the NN to make predictions.

"""

from keras.models import model_from_json
from pathlib import Path
from keras.preprocessing import image
import numpy as np
from keras.applications import vgg16

# load
f = Path("model_structure.json")
model_structure = f.read_text()
model = model_from_json(model_structure)
model.load_weights("model_weights.h5")

# Load an image file to test, resizing it to 64x64 pixels (as required by this model, set when we extract features)
img = image.load_img("dog.png", target_size=(64, 64))
image_array = image.img_to_array(img)
images = np.expand_dims(image_array, axis=0)  # keras wants a list of images

# normalize
images = vgg16.preprocess_input(images)

# Use the pre-trained NN to extract features from our test image
feature_extraction_model = vgg16.VGG16(weights='imagenet', \
                            include_top=False, input_shape=(64, 64, 3))
features = feature_extraction_model.predict(images)

# Given the extracted features of test image, make prediction using model from TL
results = model.predict(features)

# only one image, so just the first result
single_result = results[0][0]

# Print the result
print("Likelihood that this image contains a dog: {}%".format(int(single_result * 100)))