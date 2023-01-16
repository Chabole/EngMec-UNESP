import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ZebraLib as zb
from scipy.optimize import curve_fit

g = 9.81  # m/s^2
rho_agua = 997  # kg/m^3
pv_agua = 3.17e3  # kPa
P_atm = 101.325e3  # kPa
f_gen = 60  # Hz
gama = rho_agua*g

def nqa_calc(Q, Y, f_gen):
    #Veloc. espec
    nqa = 6650/np.sqrt(Y)
    # Rotação da turbina Hz
    n = (nqa*Y**(3/4))/(1000*np.sqrt(Q))
    # Polos do gerador - n deve ser inteiro
    p = round((2*f_gen)/n)
    n_new = (2*f_gen)/p
    # Recalc nqa
    nqa_new = (1000*n_new*np.sqrt(Q))/(Y**(3/4))
    return nqa_new, n_new

def modelo_turbina(H, Q, ji=5):
    # Salto energético
    Y = g*H

    # Velocidade espec.
    nqa, n = nqa_calc(Q, Y, f_gen)

    # Altura de sucção max
    sig_min = 0.28 + ((2.124e-9)*(nqa**3))
    Hsig_max = ((P_atm-pv_agua)/gama) - (sig_min*H)

    # Potência disponível
    P = rho_agua*Q*Y

    # Eficiências 1e3<P<50e3 [kW]** ~Tabela 3.2
    eta_t = 0.9
    eta_m = 0.97
    eta_v = 0.99
    eta_h = eta_t/(eta_v*eta_m)

    # Potência de eixo
    Pe = rho_agua*Q*Y*eta_h

    # Diâmetro do eixo
    Ke = 11  # ~ tau_adm=40Mpa
    deixo = Ke*(Pe/n)**(1/3)

    # Relação do cubo
    r_cubo = (7e-7*nqa**2) - (1.2e-3*nqa) + 0.8686

    # Coef e Velocidade meridiana
    Kcm = 7.1328e-3*(nqa/(np.sqrt(1-r_cubo**2)))**(2/3)
    cm = Kcm*np.sqrt(2*Y)

    # Diâmetro externo e interno
    De = np.sqrt((4*Q*eta_v)/(np.pi*cm*(1-r_cubo**2)))
    Di = De*r_cubo

    # Fixação das superficies e calc do perfil****
    j = ji # n superficies
    b = (De-Di)/j

    # Velocidade tangencial
    D = (De+Di)/2  # ***
    u = np.pi*D*n

    # velocidade absoluta entrada e a saída do rotor
    Delta_Vu = (Y*eta_h)/u

    # Veloc. corrente relat n pertubada
    W_inf = np.sqrt((u-(Delta_Vu/2))**2 + cm**2)

    # Ang construção
    beta_inf = np.arctan(cm/(u-(Delta_Vu/2)))

    # N pás e passo ~ 3, Tabela 3.3
    N = 3
    t = (np.pi*D)/N

    # Comprimento corda do perfil ***
    L_t_e = 70/(nqa**(2/3))  # dim ext
    A = 1 - Di/De
    L_t = ((1-((Di*D)/De**2))/(A))*L_t_e  # dim outros

    L = L_t*t  # talvez

    # Coeficiente de sustentação (L vem de onde ?)
    Cs = (2*Y*eta_h*cm*t)/((W_inf**2)*u*L*np.sin(beta_inf - np.deg2rad(1)))

    # fator de engrosamento ou afilamento do perfil
    r_padrão = 0.0825
    y_max = r_padrão*L
    e = (y_max/L)/(r_padrão)

    # Ang deslizamento
    ep = np.arctan(0.012 + 0.06*(y_max/L))

    # Rendimento do perfil
    eta_p = 1 - ((np.tan(ep)*W_inf)/(np.sin(beta_inf-ep)*u))

    # Ang ataque do perfil
    K1 = 0.092
    K2 = 4.8
    theta = (Cs - K1*(y_max/L))/K2

    # Ang inclinação das pás
    beta = beta_inf - theta

    # Confirmação alt sucção max
    Hsig_max_REAL = ((P_atm-pv_agua)/gama) - (0.03*Cs*(W_inf**2)) - (0.045*(cm**2))

    dic_gerais = {
        'Salto de energia':Y,
        'Velocidade específica':nqa,
        'Rotação da turbina':n,
        'Número de polos':54,
        'Coeficiente de Thoma':sig_min,
        'Altura máxima de sucção':Hsig_max_REAL,
        'Potência disponível':P,
        'Rendimento total':eta_t,
        'Rendimento mecânico':eta_m,
        'Rendimento volumétrico':eta_v,
        'Rendimento hidráulico':eta_h,
        'Potência de eixo':Pe,
        'Coeficiente de dependete da tensão':Ke,
        'Diâmetro do eixo':deixo/100,
        'Relação cúbica':r_cubo,
        'Coeficiente de veloc. meridiana':Kcm,
        'Velocidade de meridiana':cm,
        'Diâmetro externo do rotor':De,
        'Diâmetro interno do rotor':Di
    }

    dic_pa = {
        'Diâmetro':D,
        'Variação da componente de giro':Y*eta_h,
        'Velocidade tangencial':u,
        'Variação da velocidade entra/saida':Delta_Vu,
        'Velocidade da corrente não perturbada':W_inf,
        'Ângulo de construção':np.rad2deg(beta_inf),
        'Número de pás':N,
        'Passo de cada pá':t,
        'Comprimento da corda externo':L_t_e,
        'Comprimento da corda':L_t,
        'Comprimento dos perfis':L,
        'Coeficiente de sustentação':Cs,
        'Relação para escolha do perfil':y_max/L,
        'Fator de engrosamento':e, 
        'Ângulo de deslizamento':np.rad2deg(ep),
        'Rendimento do perfil':eta_p,
        'Ângulo de ataque do perfil':np.rad2deg(theta),
        'Ângulo de inclinação das pás':np.rad2deg(beta)
        }

    data_g = pd.DataFrame(dic_gerais, index=[0]).T
    data_e = pd.DataFrame(dic_pa, index=[1]).T
    return data_g, data_e