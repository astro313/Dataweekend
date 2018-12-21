import numpy as np
from keras.preprocessing import image
from keras.applications import vgg16

# Load Keras' VGG16 model that was pre-trained against the ImageNet database
model = vgg16.VGG16()

# Load the image file, resizing it to 224x224 pixels, which is the required by this model
# size of image need to match number of input nodes in the NN
img = image.load_img("bay.jpg", target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

# Normalize the input image value to the range used when training NN
x = vgg16.preprocess_input(x)

# use the deep NN model to make a prediction on x
predictions = model.predict(x)      # 1000 element, each tell us how likely the pic contains each of the 1000 obj the model was trained to recognize
predicted_classes = vgg16.decode_predictions(predictions, top=10)
print("Top predictions for this image:")

for imagenet_id, name, likelihood in predicted_classes[0]:   # index 0 since only one input image
    print("Prediction: {} - {:2f}".format(name, likelihood))

