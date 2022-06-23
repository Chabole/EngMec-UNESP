from sympy import * 
from sympy.abc import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class mola:
    def __init__(self, mat, fmax, fmin, ytrab, nf, c, sf):
        self.mat = mat
        self.fmax = fmax
        self.fmin = fmin
        self.ytrab = ytrab
        self.nf = nf
        self.c = c
        self.sf = sf

        #Dados das molas da tabela 3 - norton
        dic = { 'A227':[-0.1822, 1753.3],
                'A228':[-0.1625, 2153.5],
                'A229':[-0.1833, 1831.2],
                'A232':[-0.1453, 1909.9],
                'A232':[-0.0934, 2059.2]}
        self.b = dic[self.mat][0]
        self.A = dic[self.mat][1]

        self.Kw = ((4*self.c - 1)/(4*self.c - 4)) + 0.625/self.c
        self.Ks = (0.5/self.c) + 1
        self.Fm = (self.fmax + self.fmin)/2
        self.Fa = (self.fmax - self.fmin)/2

    @property
    def d(self):

        Ks, Kw, Fmin, Fmax, Fm, Sf, Fa, nf, Ytrab = symbols("K_s K_w F_{min} F_{max} F_m S_f F_a n_f y_{trab}") 

        #Equação iterativo de 'd'
        U = Fm-((nf-1)/nf)*Fmin
        U_ = 1.34*((A*d**b)/Sf) - 1
        J = ((8*C*nf)/(0.67*pi*A))

        d_ = (J*(Ks*U + U_*Kw*Fa))**(1/(b+2))
        
        #Cálculo iterativo do diâmetro
        solução = []
        din = 1 #chute inicial
        for i in range(10):
            s = d_.subs({d:din, Kw:self.Kw, Ks:self.Ks, Fm:self.Fm, Fa:self.Fa, nf:self.nf, Fmin:self.fmin, Fmax:self.fmax, 
                        b:self.b, A:self.A, Sf:self.sf, C:self.c, pi:np.pi})               
            solução.append(s)
            din = (s.evalf(5))
            
        return np.array(solução, dtype=float)

    def parametros(self, dc):
        #Diâmetro comercial e dados numéricos
        C, G = self.c, 80.8E9

        #Diâmetro médio D
        D = C*dc

        #Diâmetro externo D0
        D0 = D + dc

        #Rigidez da mola
        K_ = (self.fmax-self.fmin)/self.ytrab

        #Qtd de espiras ativas
        Na_ = float((G*dc**4)/(8*K_*((D)**3)))

        #aprox pra cima das qtd de espiras
        Na = int(Na_) + 1

        #Rigidez da mola de novo
        K = (G*dc**4)/(8*Na*(D)**3)

        #Deflexão inicial
        yinic = self.fmin/K

        #Comprimento livre
        Nt = Na + 2
        Lf = (dc)*Nt + 1.15*(self.ytrab) + yinic

        dic = {
            'Fm':[self.Fm],
            'Fa':[self.Fa],
            'Ks':[self.Ks],
            'Kw':[self.Kw],
            'Diâmetro médio D':[D], 
            'Diâmetro externo D0':[D0],
            'K':[K],
            'Na':[Na],
            'yinic':[yinic],
            '---- Resumo dos parâmetros -----'
            'Material':[self.mat], 
            'Diâmetro comercial':[dc],
            'Diâmetro externo':[D0],
            'Número total de espiras':[Nt],
            'Comprimento livre':[Lf]}

        df = pd.DataFrame.from_dict(dic)
        return df.T



molas = mola('A227', 150*4.44822, 100*4.44822, 0.75*0.0254, 2, 8, 310)
print(molas.parametros(6.5E-3))
