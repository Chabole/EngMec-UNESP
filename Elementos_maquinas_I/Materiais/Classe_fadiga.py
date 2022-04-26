# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 17:38:59 2021
Version __0.0.1__

@author: Arthur Chabole
Classe Material para calcular resistência a fadiga corrigido e outras propriedades do material. [em desenvolvimento]
"""

import numpy as np
import pandas as pd

class Material():
    
    def __init__(self, material,
                 Sult, 
                 HB=None, 
                 kind='flexão', 
                 acabamento='retificado', 
                 c='99',
                 d=862,
                 T=30):
        '''
        Parameters
        ----------
        material : string
            Nome do material: aço, ferros, alumínio e cobre.
        HB : string
            Dureza Brinell.
        kind : string, optional
            Tipo de carregamento: Flexão, normal ou torção. The default is 'flexão'.
        acabamento : string, optional
            Acabamento superficial retificado, laminado, forjado, usinado. The default is 'retificado'.
        c : string, optional
            Intervalo de confiança. The default is '99'.
        d : float, optional
            Diâmetro do material. The default is 862.
        T : float, optional
            Temperatura. The default is 30.

        Returns
        -------
        Object.

        '''
                
        self.material = material
        
        if HB == None:
            self.Sult = Sult
        else:
            #Estimar Limite de resistência a tração (Sult)
            self.HB = HB
            self.Sult = ((500*HB)/1000)*6.89476 #[Mpa]
    
        self.kind = kind
        self.acabamento = acabamento
        self.c = c
        self.d = d
        self.T = T
        
        #Dados dos materiais
        self.Carga = {'flexão':0.9, 'normal':0.75, 'torção':0.72}
        
        #Estimar Limite de resistência a fadiga (Sf)
        self.Sf = self.__Sf()
        
        #Estimar Limite de resistência a fadiga corrigido (S'f)
        self.S_f = self.Sf_corrigido
        
        #Coeficientes
        self.b_corr = - np.log10((self.Sult*self.Carga[self.kind]/self.S_f)**(1/3))
        self.b_ncorr = - np.log10((self.Sult*self.Carga[self.kind]/self.Sf)**(1/3))
        
    #Estimar Limite de resistência a fadiga corrigido (S'f)
    @property
    def Sf_corrigido(self):
          self.__Ka = {'flexão':1, 'normal':0.70, 'torção':0.557}
          self.__Kd = {'50':1, '90':0.897, '95':0.868, '99':0.814, '99.9':0.753, '99.99':0.702, '99.999':0.659, '99.9999':0.620}
          
          #Calculando os K's
          self.Ka = self.__Ka[self.kind]
          self.Kb = self.__Kb()
          self.Kc = self.__Kc()
          self.Kd = self.__Kd[self.c]
          self.Ke = self.__Ke()

          return self.Ka*self.Kb*self.Kc*self.Kd*self.Ke*self.Sf
      
    def regra_Miner(self, ciclo_sigma):
        '''
        
        Calcula o número de ciclos até a falha por fadiga utilizando a regra de miner.
        
        Parameters
        ----------
        ciclo_sigma : list or tupla (N, Mpa)
            Tupla com os valores de (ciclos, tensão). Exemplo: [(1, 100), (2, 90)]

        Returns
        -------
        float
            Número de ciclos até a falha por fadiga.
            
        Example
        -------
        >>> Material = S_fadiga('aço', 310, 
                                acabamento='retificado', 
                                kind='flexão', c='50', d=5)
        
        1 ciclo de 100Mpa, 2 ciclos de 90Mpa e 5 ciclos de 80Mpa.
        
        >>> ciclos = Material.regra_Miner([(1, 100), 
                                           (2, 90), 
                                           (5, 80)])
            10343 ciclos
            
        >>> Horas = (ciclos*20)/3600
            57 horas

        '''
        #Convertendo de Mpa pra Ksi
        #S'ut
        S_ult = (self.Carga[self.kind]*self.Sult/6.89476)*1000
        
        #S'f
        S_f = (self.S_f/6.89476)*1000
        
        #Definindo coef da curva S-N
        m = np.log10((S_ult/S_f)**(1/3))
        b = np.log10((S_ult**2)/S_f)
        
        #Aplicando a regra de miner
        acum = 0
        for lista in ciclo_sigma:
            ciclo, sigma = lista
            n = 10**(- ((np.log10(sigma*1E+3) - b)/m))
            acum += ciclo/n
        ciclos_totais = 1/acum
        return ciclos_totais
    
    def tensão_ToFalha(self, N, correção=True):
        '''
        
        Cálcula a tensão máxima de trabalho dado um número de ciclos. 

        Parameters
        ----------
        N : float or array
            Número de ciclos.

        Returns
        -------
        sigma : float or array
            Tensão máxima de trabalho.

        '''
        if correção:
            b = self.b_corr
        else:
            b = self.b_ncorr
            
        a = 10**(np.log10(self.Sult*self.Carga[self.kind]) - 3*b) 
        sigma = a*(N**b)
        return sigma
    
    def ciclos_ToFalha(self, sigma):
        '''
        
        Calcula o número de ciclos até a falha por fadiga do material dado a tensão de trabalho.

        Parameters
        ----------
        sigma : float or array
            Tensão de trabalho.

        Returns
        -------
        ciclos : float
            Número de ciclos minimos até a falha por fadiga.

        '''
        a = 10**(np.log10(self.Sult*self.Carga[self.kind]) - 3*self.b_corr) 
        ciclos = (sigma/a)**(1/self.b_corr)
        return ciclos
            
    def diagrama_SN(self, ciclos, limite_fadiga= 1E+6, correção=True):
        '''
        Calcula o diagrama S-N do material.

        Parameters
        ----------
        ciclos : array
            Array com os número de ciclos.
        limite_fadiga : float, optional
            Limite fadiga para o material. The default is 1E+3.

        Returns
        -------
        sigma : array
            Tensão.

        '''
        sigma = []
        for N in ciclos:
            if N > limite_fadiga:
                if correção:
                    sigma.append(self.S_f) #S_f
                else:
                    sigma.append(self.Sf) #S_f
            else:
                sigma.append(self.tensão_ToFalha(N, correção))
        return sigma
    
    def info(self, local=None):
          tabela=[]
          tabela.append({
              
              'INPUTS':'---------',
              'Material':self.material,
              #'Dureza HB':self.HB,
              'Diâmetro':self.d,
              'Sult':self.Sult,
              'Acabamento':self.acabamento,
              'Confiança':float(self.c),
              'Carga':self.kind,
              'Temperatura':self.T,
              
              'OUTPUTS':'---------',
              'Sf':self.Sf,
              'Ka':self.__Ka[self.kind],
              'Kb':self.__Kb(),
              'Kc':self.__Kc(),
              'Kd':self.__Kd[self.c],
              'Ke':self.__Ke(),
              "Sf'":self.S_f
              })
          df = (pd.DataFrame(tabela).T)
          df.columns = ['Valores']
          if local == None:
              pass
          else:
              df.to_excel(local)
          return df

    #Estimar Limite de resistência a fadiga (Sf)
    def __Sf(self):
        def materiais():
            return {'aço':[0.5*self.Sult, 1400, 700], 
                    'ferros':[0.4*self.Sult, 400, 160], 
                    'alumínios':[0.4*self.Sult,330, 130], 
                    'cobre':[0.4*self.Sult,280, 100]}.get(self.material, 'Erro')
        
        if (self.Sult < materiais()[1]):
            return materiais()[0]
        else:
            return materiais()[2]
      
    def __Kc(self):
        def acabamento_superf():
            return {'retificado':[1.58, -0.085], 
                    'usinado':[4.51, -0.265], 
                    'laminado':[57.7, -0.718], 
                    'forjado':[272, -0.995]}.get(self.acabamento, 'Erro')
        
        A, b = acabamento_superf()
        return A*self.Sult**(b) #*1.03 Talvez precise dessa correção
    
    def __Kb(self):
      if self.d <= 7.62 or self.kind == 'normal':
        Kb = 1
      if (self.d > 7.62) and (self.d <= 250):
        Kb = 1.189*self.d**(-0.097)
      if (self.d > 250):
        Kb = 0.6          
      return Kb
    
    def __Ke(self):
      if self.T <= 450:
        Ke = 1
      if (self.T > 450) and (self.T <= 550):
        Ke = 1 - (0.0058*(self.T-450))
      return Ke


