import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
from uncertainties import ufloat
from uncertainties.umath import *  # sin(), etc.
import ZebraLib as zb
import uncertainties.unumpy as un

rho_agua, rho_ar, g = 997, 1.2, 9.81 #kg/m^3 e m^2/s
mi = 1.9e-5                         #visc. cinemática ar 25°C

#MEC FLU II
def incert_A(array):
    '''
    Calcula a incerteza do tipo A dado uma array form numpy.
    
    '''
    return ufloat(array.mean(), array.std(ddof=1)/np.sqrt(len(array)))

def perda_carga(delta_h):
    '''
    Calcula a perda de carga hl dado  
    diferença de H do tubo em U [cm] com água.
    '''
    delta_P = rho_agua*g*(delta_h/100)
    return delta_P/rho_ar

def h2v(delta_h):
    '''
    Cácula velocidade s/ correção [m/s] para tubo de venturi ou
      placa de orificio dado diferença de H do tubo em U [cm] com água.
    '''
    return np.sqrt((2*rho_agua*g*(delta_h/100))/rho_ar)

def df_calc_vazão(df, prop=3):
    nome_coluna = df.columns
    lista = []
    for i in range(len(nome_coluna)):
        lista.append(calc_vazão(df[nome_coluna[i]].values)[prop])
    arr = np.array(lista)
    return pd.DataFrame(arr.T, columns=df.columns)

def calc_vazão(delta_h, D1=0.0385, Dt=0.0257, venturi=False, beta=None):
    '''
    Cálcula velocidade c/ correção (+ outros parâmetros de convergência) para tubo de venturi
      ou placa de orificio dado diferença de H do tubo em U [cm] com água.
    '''
    if beta:
        pass
    else: 
        beta = Dt/D1

    At = np.pi*(Dt**2)/4
    A1 = np.pi*(D1**2)/4

    delta_P = rho_agua*g*(delta_h/100)

    lista_m, lista_Re, lista_k = [], [], []
    for j in range(len(delta_P)):
        m_dot  = 1.0
        for i in range(100):

            v = m_dot/(rho_ar*A1)
            Re = (rho_ar*v*D1)/mi

            if venturi:
                C = 1.0011 + 0.0123*beta - 0.0169*np.e**(-0.4*Re/1e5)
            else:
                C = 0.5959 + (0.0312*(beta**2.1)) - (0.184*beta**8) + ((91.71*beta**2.5)/(Re**0.75))

            K = C/np.sqrt(1 - beta**4)
            m_dot_new = K*At*np.sqrt(2*rho_ar*(delta_P[j]))
            
            if abs(m_dot - m_dot_new) < 1e-8:
                break
            else:
                m_dot = m_dot_new

        lista_m.append(m_dot_new)
        lista_Re.append(Re)
        lista_k.append(K)
        
    lista_m = np.array(lista_m)
    lista_Re = np.array(lista_Re)
    lista_k = np.array(lista_k)
    lista_Q = lista_m/rho_ar
    lista_V = lista_Q/A1
    return lista_m, lista_Q, lista_V, lista_Re, lista_k, beta #kg/s, m^3/s, m/s

# TURBO MAQUINAS

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
        return (self.ps-self.pe)/(rho_agua*g)
    @property
    def hu(self):
        A = (self.ps - self.pe)/(rho_agua*g)
        B = ((self.vs**2) - (self.ve**2))/(2*g)
        return A + B + (self.zs - self.ze)

    def ph(self, Q):
        return Q*rho_agua*g*self.hu

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

def error(x, y, mark, tipo, ax):
    ax.errorbar(y=un.nominal_values(y), 
    x=un.nominal_values(x), yerr=un.std_devs(y), 
    xerr=un.std_devs(x), 
    fmt=mark, capsize=5, markersize=7,  
    markeredgecolor='black', ecolor='black', label=f'{tipo}')