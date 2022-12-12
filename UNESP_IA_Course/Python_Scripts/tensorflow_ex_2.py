# -------------------------------------------------------------------
# tensorflow_ex_2.py
# -------------------------------------------------------------------
# Create values and compute y = ax + b using TensorFlow.
# Plot y versus x using Matplotlib.
# -------------------------------------------------------------------

# -------------------------------------------------------
# Modules to import
# -------------------------------------------------------

import tensorflow as tf
import matplotlib.pyplot as plt

# -------------------------------------------------------

a = tf.constant(5.)
b = tf.constant(-3.)
x = tf.constant(tf.linspace(-5.0, 5.0, 11))

# y = (a*x) + b
y = tf.add(tf.multiply(a, x), b)

print(a)
print(b)
print(x)
print(y)

plt.plot(x, y, 'b-')
plt.plot(x, y, 'ro')
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of y = ax + b')
plt.show()

# -------------------------------------------------------------------
# End of file
# -------------------------------------------------------------------
