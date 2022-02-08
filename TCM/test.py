
import numpy as np
import matplotlib.pyplot as plt

def area_p(d, L):
    r = d/2
    return 2*np.pi*r*L #2*np.pi*(r**2) + 

def area_g(d, L):
    r = d/2
    return 2*np.pi*r*L + 2*np.pi*(r**2) 

def sei(x, y):
    A = 50/x
    return x*y+A


print('olá, mundo!')

print(sei(4,6))
T = sei(5, 6)
H = area_g(4, 5)
print('oi')