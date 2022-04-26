# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:44:51 2021

@author: Arthur Chabole
Meu recebi um e-mail que o meu boleto já foi pago. O um atendente informou que guardo isso acontecesse era pra entregar em contato com vcs.  Já posso tentar me cadastrar no spotify de novo ?
"""

import numpy as np 
import matplotlib.pyplot as plt
import Classe_fadiga as fd

#%% Célula para o cálculo de Sf' TESTE 2

#Criar o material
Mat = fd.Material('aço', Sult=140/0.145,
                kind='normal', acabamento='usinado',
                c='99', d=0.0)

Sf_= Mat.Sf_corrigido
Sf = Mat.Sult

Nf= 1.2
kt=3.25

sigma_max = (2*Mat.Sf_corrigido*Mat.Sult)/(Nf*(Mat.Sf_corrigido + Mat.Sult))
sigma_m = sigma_max/2

#Dados
b=0.382*25.4
d=0.125*25.4
h=0.050*25.4

L = ((b-d)*h)
A = (Sf_*Sf) - (sigma_m*Sf_*Nf)
K = kt*Sf*Nf

P = (A*L)/(K)
print(P)

#sigma_n = P/((b-d)*h)

#%% Célula para o cálculo de Sf' TESTE 1
W=3*25.4
h=0.5*25.4
d = h

#Definir diâmetro equivalente
D_eq = ((0.05*W*h)/(0.0766))**0.5

#Criar o material
Mat = fd.Material('aço', Sult=140/0.145,
                kind='flexão', acabamento='usinado',
                c='90', d=D_eq)

#Sf'
Sf_c = Mat.S_f

#Coeficientes
A = 2.24
b= -0.78739 #Tabela do exercicio

#Fator de correção
Nf = 2
Kt= A*(np.e**(b*(d/W)))

sigma_nom= (6/((W-d)*(h**2))) #O exercicio fornece a equação

sigma_real=Kt*sigma_nom # acrescimo do Kt

M1=Sf_c/(Nf*sigma_real) #Newtons
M2=M1/1000 #N para kN

print(M2)

#%% Célula do gráfico 
#Valores de ciclos e tipo de acabamento
Superficies = ['usinado', 'retificado', 'forjado', 'laminado']
ciclos = np.array((1, 10, 100, 1E3, 1E4, 1E5, 1E6, 1E7, 1E8))

#Gráfico - cosméticos
fig, ax = plt.subplots(figsize=(10,7))
ax.set(title='Diagrama S-N', 
        xlabel=r'Ciclos [$N$]', ylabel=r'Tensão $\sigma$')

#Plotando pra diferentes acabamentos
#Com correção de resistência a fadiga
for superf in (Superficies):
    Mat = fd.Material('aço', Sult=600,
                kind='flexão', acabamento=superf,
                c='99', d=25)
    
    sigma = Mat.diagrama_SN(ciclos)
    #print(f'Acabamento={Mat.acabamento} e Ciclos={Mat.ciclos_ToFalha(300)}')
    
    ax.scatter(ciclos, sigma)
    ax.plot(ciclos, sigma, label=f'{Mat.acabamento} e '  + r"$S_f'$=" + f'{Mat.S_f:.0f}Mpa')

#Sem correção de resistência a fadiga
sigma = Mat.diagrama_SN(ciclos, correção=False)
ax.scatter(ciclos, sigma)
ax.plot(ciclos, sigma, '--', label='sem correção')

#Deixando bonito
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(0.9E2, 1E3)
ax.set_xlim(1E+3, 1E8)
ax.legend()
ax.grid(linestyle='dotted')

#fig.savefig('D:/UNESP/PythonImagineers/diagrama_SN.pdf')