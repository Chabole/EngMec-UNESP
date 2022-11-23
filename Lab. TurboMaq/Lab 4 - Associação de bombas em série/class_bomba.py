import numpy as np
import matplotlib.pyplot as plt
from uncertainties import ufloat
from uncertainties.umath import *  # sin(), etc.
import uncertainties.unumpy as un

rho, g = 997, 9.8067

class bomba:

    def __init__(self, pe, ps, ve, vs, ze, zs):
        self.pe = pe
        self.ps = ps
        self.ve = ve
        self.vs = vs
        self.ze = ze
        self.zs = zs

    @property
    def hm(self):
        return (self.ps-self.pe)/(rho*g)
    @property
    def hu(self):
        A = (self.ps - self.pe)/(rho*g)
        B = ((self.vs**2) - (self.ve**2))/(2*g)
        return A + B + (self.zs - self.ze)

    def ph(self, Q):
        return Q*rho*g*self.hu

    def psi_m(self, w, D):
        C_psi = 8
        return C_psi*((g*self.hm)/((D**2)*(w**2)))

    def psi_u(self, w, D):
        C_psi = 8
        return C_psi*((g*self.hu)/((D**2)*(w**2)))

    def nq_m(self, Q, w):
        Cnq = ((30*g)**(3/4))/np.pi
        return Cnq*(w*un.sqrt(Q)/(g*self.hm)**(3/4))

    def nq_u(self, Q, w):
        Cnq = ((30*g)**(3/4))/np.pi
        return Cnq*(w*un.sqrt(Q)/(g*self.hu)**(3/4))

    def phi(self, Q, w, D):
        C_phi = 63369.75
        return C_phi*(Q/(w*D**3))

    def Re(self, w, D, v):
        return (w*D**2)/(v)

def Q2v(Q, D):
    '''
    Q[m^3/h] e D[m]
    '''
    q = Q/3600 #m^3/s
    r = D/2    #m
    return q/(np.pi*(r**2))

def incert_A(array):
    return ufloat(array.mean(), array.std(ddof=1)/np.sqrt(len(array)))

def error(x, y, mark, tipo, ax):
    ax.errorbar(y=un.nominal_values(y), 
    x=un.nominal_values(x), yerr=un.std_devs(y), 
    xerr=un.std_devs(x), 
    fmt=mark, capsize=5, markersize=7,  
    markeredgecolor='black', ecolor='black', label=f'{tipo}')