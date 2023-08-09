import fortunae as ft
import pandas as pd
import time 
import json
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

stocks = pd.read_excel('D:/UNESP/Finance/outputs.xlsx', index_col=0)
fiis = pd.read_excel('D:/UNESP/Finance/outputs.xlsx', sheet_name='FIIs', index_col=0)

def search_seg_ativo(ID):
    seg = []
    for i in range(len(ID)):
        seg.append(stocks[stocks['Ativo']==ID[i]]['Subsetor de Atuação'].values[0])
    return seg

def search_by_category(segmentos):
    df = pd.DataFrame()
    for i in segmentos:
        f1 = stocks[(stocks['Subsetor de Atuação'] == i)]
        df = df.append(f1)
    return df

def compare_df(stocks):
    lista_ID = stocks.Ativo.values
    df_total = pd.DataFrame()
    for id in range(len(lista_ID)):
        ativo_iterado =  stocks.Ativo.values[id]

        #Encontrando o subsetor pelo nome do ativo
        seg = search_seg_ativo([ativo_iterado])

        #Encontrando o valores médios dos parametros do subsetor
        df_grup = stocks.groupby(by='Subsetor de Atuação')
        Ativo_classe = df_grup.mean().loc[seg]

        #COMO FAZER UMA DIVISÃO ENTRE OS DADOS DE CIMA
        cols = Ativo_classe.columns
        res = []
        for i in range(len(cols)):
            try:
                ativo = (float(stocks[stocks.Ativo == ativo_iterado][cols[i]]))
                setor = (float(Ativo_classe[cols[i]]))
                res.append((setor-ativo)/setor)
            except:
                res.append(69.99)
        df_dif = pd.DataFrame(np.asarray(res).reshape(1, len(cols)), columns=cols)

        df_dif.insert(loc=0, column='Ativo', value=ativo_iterado)
        df_dif.insert(loc=1, column='Subsetor de Atuação', value=seg[0])

        df_total = df_total.append(df_dif)
    return df_total

#'P/VP', 'P/L', 'D.Y', 'LPA', 'ROE'
#df['P/L'][['max', 'min']]
#stocks[stocks['Subsetor de Atuação']=='Serviços'][['Ativo', 'P/VP']]
#stocks['Subsetor de Atuação'].unique()
#stocks.columns.values
#stocks.head(3)