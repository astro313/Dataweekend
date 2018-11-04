import numpy as np
from keras.preprocessing import image
from keras.applications import resnet50

# Load Keras' ResNet50 model that was pre-trained against the ImageNet database
model = resnet50.ResNet50()

# Load image, resizing to 224x224 pixels (required by this model)
# Note size of img needs to match number of input nodes in the NN
img = image.load_img("bay.jpg", target_size=(224, 224))
import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()

# Convert the image to a numpy array
# (x,y),RGB
x = image.img_to_array(img)

# Add a forth dimension since Keras expects a list of images
x = np.expand_dims(x, axis=0)

# re-scale/normalize input image to the range used in the trained network
x = resnet50.preprocess_input(x)
predictions = model.predict(x)

# Look up names of top 9 matches of the predicted classes
predicted_classes = resnet50.decode_predictions(predictions, top=9)
# 1000 element array of floats, each tells the likelihood that the image contain each of the 1000 object the model is trained to recognized

print("This is an image of:")

# results for the first image.
for imagenet_id, name, likelihood in predicted_classes[0]:
    print(" - {}: {:2f} likelihood".format(name, likelihood))

