# -------------------------------------------------------------------
# numpy_ex_2.py
# -------------------------------------------------------------------
# Create values and compute y = ax + b using NumPy.
# Plot y versus x using Matplotlib.
# -------------------------------------------------------------------

# -------------------------------------------------------
# Modules to import
# -------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------

a = 5.0
b = -3.0
x = np.linspace(-5.0, 5.0, 11, endpoint=True)

# y = (a*x) + b
y = np.add(np.multiply(a, x), b)

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
