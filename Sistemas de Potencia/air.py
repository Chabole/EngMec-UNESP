import numpy as np
import pandas as pd
import ZebraLib as zb

def _regression(key, value):
    '''
    Faz a interpolação dos valores termodinâmicos pela tabela A-22 do shapiro. Método interno.

    Parameters
    ----------
    key : list
        Propriedade termodinâmica ('T', 'h', 'u', 's', 'pr', 'vr') e valor. Example: ['T', 1300].
    value : string 
        Propriedade termodinâmica que deseja encontrar.

    Returns
    -------
    valor : float
        Valor interpolado por regressão linear da propriedade "value" escolhida.

    Example
    -------
    >>> import air 
    >>> air.air_regression(['T', 551], 'u')
    397.63 #kJ/kg

    >>> air.air_regression(['vr', 551], 's')
    1.75 #kJ/kg.K

    >>> air.air_regression(['vr', 551], 'T')
    314.83 #K
    '''

    #Importando os dados e encontrando a posição do valor mais próximo
    df = pd.read_excel('D:/UNESP/PythonImagineers/Termo/ideal_air_data.xlsx')
    index_line = zb.get_index_of_nearest_element(df[key[0]].values, key[1])

    #Localizando as linhas mais próximas 
    column = [df.loc[index_line-1], df.loc[index_line], df.loc[index_line+1]]

    #Fazendo lista dos valores das propriedades x e y para interpolar
    x = [column[0][key[0]], column[1][key[0]], column[2][key[0]]]
    y = [column[0][value], column[1][value], column[2][value]]
    valor = zb.fit(x, y, 1)(key[1])
    return valor

def linear_regression(key):
    '''
    Faz a interpolação dos valores termodinâmicos pela tabela A-22 do shapiro.

    Parameters
    ----------
    key : list
        Propriedade termodinâmica ('T', 'h', 'u', 's', 'pr', 'vr') e valor. Example: ['T', 1300].

    Returns
    -------
    df : pd.DataFrame
        Valores interpolado por regressão linear da propriedades termodinâmicas.

    Example
    -------
    >>> import air 
    >>> air.air_regression(['T', 551])
    T           h           u           s       pr      vr
    314.8246	315.0904	224.7142	1.7504	1.6422	551.0
    '''
    propriedades = ['T', 'h', 'u', 's', 'pr', 'vr']
    interpol = []
    for prop in propriedades:
        interpol.append(round(_regression_hand(key, prop), 4))
    df = pd.DataFrame(interpol, propriedades).T
    return df
    
def _regression_hand(key, value):

    #Importando os dados e encontrando a posição do valor mais próximo
    df = pd.read_excel('D:/UNESP/PythonImagineers/Termo/ideal_air_data.xlsx')
    index_line = zb.get_index_of_nearest_element(df[key[0]].values, key[1])

    #Localizando as linhas mais próximas 
    column = [df.loc[index_line-1], df.loc[index_line], df.loc[index_line+1]]

    #Verificando qual dos valores das pontas são menores
    valor_0 = (abs(column[0][key[0]]))
    valor_2 = (abs(column[2][key[0]]))   

    if valor_0 > valor_2:
        index = 0
    else:
        index = 2

    #Fazendo lista dos valores das propriedades x e y para interpolar
    x = [column[index][key[0]], column[1][key[0]]]
    y = [column[index][value], column[1][value]]
    valor = zb.fit(x, y, 1)(key[1])
    return valor