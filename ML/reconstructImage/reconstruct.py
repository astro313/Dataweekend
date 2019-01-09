"""
Reconstructing pictures with machine learning

adapted from http://arogozhnikov.github.io/2016/02/09/DrawingPictureWithML.html

Train on a subset of pixels of an image (single color) using different regression algorithms, try to reconstruct the original picture.


Use scikit-learn

"""


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, GradientBoostingRegressor, AdaBoostRegressor

from sklearn.cross_validation import train_test_split
from sklearn.random_projection import GaussianRandomProjection
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.kernel_approximation import RBFSampler
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

# can't install theanets
# from rep.metaml import FoldingRegressor
# from rep.estimators import XGBoostRegressor, TheanetsRegressor

import os
os.system('wget http://static.boredpanda.com/blog/wp-content/uploads/2014/08/cat-looking-at-you-black-and-white-photography-1.jpg  -O image.jpg')

# each image has (x, y) coordinate and intensity of pixel
print np.asarray(Image.open('./image.jpg')).shape        # (542, 880, 3)
img = np.asarray(Image.open('./image.jpg')).mean(axis=2)


plt.figure()
plt.imshow(img, cmap='gray')


def train_display(regressor, image, train_size=0.02):
    """
        a func to train regressor.

    Parameters
    ----------
    regressor: function

    image: 2D array

    train_size: float
        fraction of pixels used for training

    """
    height, width = image.shape
    flat_image = image.reshape(-1)

    # get indices of pixels
    xs = np.arange(len(flat_image)) % width
    ys = np.arange(len(flat_image)) // width
    data = np.array([xs, ys]).T         # train data format, nrow x 2

    target = flat_image                 # pixel value

    # split into train and test sets
    trainX, testX, trainY, testY = train_test_split(data, target, \
                                                    train_size=train_size, \
                                                    random_state=42)
    mean = trainY.mean()
    regressor.fit(trainX, trainY - mean)
    new_flat_picture = regressor.predict(data) + mean

    plt.figure(figsize=[20, 10])
    plt.subplot(121)
    plt.imshow(image, cmap='gray')    # input
    plt.subplot(122)
    plt.imshow(new_flat_picture.reshape(height, width), cmap='gray')
    plt.show()


# linear regression
train_display(LinearRegression(), img)

# decision tree
train_display(DecisionTreeRegressor(max_depth=10), img)
train_display(DecisionTreeRegressor(max_depth=20), img)

# deicison tree limited by minimal number of sample in a leaf
train_display(DecisionTreeRegressor(min_samples_leaf=40), img)
train_display(DecisionTreeRegressor(min_samples_leaf=5), img)

# random forest
train_display(RandomForestRegressor(n_estimators=100), img)

# KNN
train_display(KNeighborsRegressor(n_neighbors=2), img)
# more neighbours + weighting according to distance
train_display(KNeighborsRegressor(n_neighbors=5, weights='distance'), img)
train_display(KNeighborsRegressor(n_neighbors=25, weights='distance'), img)

# KNN
train_display(KNeighborsRegressor(n_neighbors=2, metric='canberra'), img)

# # gradient boosting
# train_display(XGBoostRegressor(max_depth=5, \
#                                n_estimators=100, \
#                                subsample=0.5, nthreads=4), img)

# # Gradient Boosting with deep trees
# train_display(XGBoostRegressor(max_depth=12, n_estimators=100, \
#                                subsample=0.5, nthreads=4, eta=0.1), img)

# # NN
# train_display(TheanetsRegressor(layers=[20, 20], hidden_activation='tanh',
#                                 trainers=[{'algo': 'adadelta', 'learning_rate': 0.01}]), img)

# AdaBoost over Decision Trees using random projections
base = make_pipeline(GaussianRandomProjection(n_components=10),
                     DecisionTreeRegressor(max_depth=10, max_features=5))
train_display(AdaBoostRegressor(base, n_estimators=50, learning_rate=0.05), img)

# Bagging over decision trees using random projections, sometimes referred as Random Forest
base = make_pipeline(GaussianRandomProjection(n_components=15),
                     DecisionTreeRegressor(max_depth=12, max_features=5))
train_display(BaggingRegressor(base, n_estimators=100), img)


