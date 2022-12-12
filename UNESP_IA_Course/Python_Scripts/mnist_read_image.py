# ---------------------------------------------------------------
# mnist_read_image.py
# ---------------------------------------------------------------
# Load the MNIST dataset and view the first image in the training
# data.
# ---------------------------------------------------------------

# ------------------------------------------------------
# Modules to import
# ------------------------------------------------------

import tensorflow as tf
import matplotlib.pyplot as plt

dataset = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = dataset.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

print('-- Train and Test -----------------------------')
print('>> Train: x=%s, y=%s' % (x_train.shape, y_train.shape))
print('>> Test : x=%s, y=%s' % (x_test.shape, y_test.shape))

print('-- x_train[0] ---------------------------------')
print(x_train[0])
print('-- y_train[0] ---------------------------------')
print(y_train[0])
print('-----------------------------------------------')

plt.imshow(x_train[0])
plt.show()

# ---------------------------------------------------------------
# End of file
# ---------------------------------------------------------------
