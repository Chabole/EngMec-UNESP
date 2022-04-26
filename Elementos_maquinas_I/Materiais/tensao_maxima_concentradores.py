
import numpy as np
import time
import math

#conversoes
mm=25.4
Pa_Ksi=0.145

#DADOS
Tipo_aço= "usinado"
sigma_m=0 #TOTALMENTE ALTERNADO
W=3*mm #mm
h=0.5*mm #mm
d=0.5*mm #mm
b=-0.78739 #Tabela do exercicio
A=2.24 #Tabela do exercicio
conf=90 #%
Nf=2 
Sut=140/Pa_Ksi #MPa
Sf=0.5*Sut # Pois Sut<1400MPa
D=np.sqrt((0.05*W*h)/0.0766) #Diametro equivalente
Ka=1 #Pois o carregamento é FLEXAO
Kb=0.869*D**(-0.097) #pois 0.3<D<10 polegadas ou 7.62<D<254mm
Kc=0.718 #peguei da tabela para Sut= 140Ksi OBS: como Kc é coeficiente, não importa se vc ta trabalhando com Ksi ou MPa
Kd=0.897 #Confiabilidade de 90%
Sf_c=Ka*Kb*Kc*Kd*Sf

Kt=2.24*math.e**((b*(d/W))) #Kt para d/h>=0.25

sigma_nom=(6/((W-d)*h**2)) #O exercicio fornece a equação

#OBS DO SIGMA_NOM:

#Qnd vc usa MPa(Pa*10E6) vc devee usar os dados em mm, pois fração de MPa/mm*mm as potencias 10E6 se cancelam
#E assim o resultado será dado em N

sigma_real=Kt*sigma_nom # acrescimo do Kt
sigma_a=sigma_real #não sei o porque, so aceitei
M1=Sf_c/(Nf*sigma_real) #Newtons
M2=M1/1000 #N para kN
print("==================================================================")
print("M = %f N, ou M= %f kN"%(M1,M2))



