import fortunae as ft
import pandas as pd
import time 
import json
import matplotlib.pyplot as plt
import plotly.express as px


start = time.time()

#Pegando a lista de ações e fundos
ações =  pd.read_excel('D:/UNESP/Finance/ID_acoes.xlsx').values #473 ações
#fiis = ft.br_fiis()    #250 fundos

#Scraping de dados usando threads
df_ações = ft.get_stocks(ações)
#df_fiis = ft.get_fiis(fiis)

#Gravando os resultados
with pd.ExcelWriter('outputs.xlsx') as writer:  
    df_ações.to_excel(writer, sheet_name='acoes')
    #df_fiis.to_excel(writer, sheet_name='FIIs')
    
print(f'Tempo de processamento gasto {(time.time() - start):.3f}s')



'''
df_ações = pd.read_excel('D:/UNESP/Finance/outputs.xlsx')

df_ações = df_ações[(df_ações['VOLUME (dia)'] >=0.5e6) & (df_ações['P/L']>0) & (df_ações['P/L']<100)]
fig = px.scatter(df_ações, x="D.Y", y="Subsetor de Atuação", color="Setor de Atuação",
                 size='ROE', hover_data=['Ativo'])
fig.show()

seg = search_seg_ativo(['MGLU3'])

#Encontrando o valores médios dos parametros do subsetor
df_grup = stocks.groupby(by='Subsetor de Atuação')
Ativo_classe = df_grup.mean().loc[seg]
Ativo_classe

Ativo_classe = Ativo_classe.reset_index()
Ativo_classe.rename(columns={'Subsetor de Atuação': 'Ativo'}, inplace=True)

ativo = stocks[stocks.Ativo=='MGLU3'].drop(columns=['Setor de Atuação', 'Subsetor de Atuação','Segmento de Atuação'])
ativo
#Ativo_classe.append(ativo)'''