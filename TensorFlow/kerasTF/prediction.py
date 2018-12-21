from keras.models import model_from_json
from pathlib import Path
from keras.preprocessing import image
import numpy as np

# These are the CIFAR10 class labels from the training data (in order from 0 to 9)
class_labels = [
    "Plane",
    "Car",
    "Bird",
    "Cat",
    "Deer",
    "Dog",
    "Frog",
    "Horse",
    "Boat",
    "Truck"
]

# Load model's structure's NN
f = Path("model_structure.json")
model_structure = f.read_text()

# Recreate Keras model object
model = model_from_json(model_structure)

# Re-load the model's trained weights
model.load_weights("model_weights.h5")

# Load a test img
img = image.load_img("car.png", target_size=(32, 32))

# load to 3D
image_to_test = image.img_to_array(img)
list_of_images = np.expand_dims(image_to_test, axis=0)    # [list of images, 3D of the images]

# predict using model
results = model.predict(list_of_images)

# since only testing one image, only need to check the 1st result
single_result = results[0]

print(len(single_result))
print(len(class_labels))

# We will get a likelihood score for all 10 possible classes. Find out which class had the highest score.
most_likely_class_index = int(np.argmax(single_result))
class_likelihood = single_result[most_likely_class_index]
class_label = class_labels[most_likely_class_index]

print("This is image is a {} - Likelihood: {:2f}".format(class_label, class_likelihood))