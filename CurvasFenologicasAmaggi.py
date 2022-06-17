#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[1]:


import pandas as pd 
import numpy as np 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from datetime import date


# ##  Abrindo CSV

# In[2]:


#Abrindo a tabela em csv 
tabela = pd.read_csv('relatorio_resultados_14-06-2022.csv', sep=';')
tabela = tabela.rename_axis('ID').reset_index()


# In[3]:


tabela.head()


# ## Gráfico Curva Fenológica 

# In[4]:


#Barra Lateral
barra_lateral = st.sidebar.empty()
image = Image.open('Logo-Escuro.png')
st.sidebar.image(image)
st.sidebar.markdown('### Avaliação Fenológica do Algodão por meio de Índices de Vegetação')

#Selecionar Fazenda
filtro_fazenda = st.sidebar.selectbox('🚜 Selecione a Fazenda:',('Faz. Água Quente','Faz. Tucunaré','Faz. Itamaraty'))
tabela_fazenda = tabela['Fazenda'] == filtro_fazenda
tabela_fazenda = tabela[tabela_fazenda]

#Selecionar Talhão 
filtro_talhao = st.sidebar.selectbox('🔲 Selecione o Talhão:',(tabela_fazenda['Talhão']))
tabela_talhao = tabela_fazenda['Talhão'] == filtro_talhao
tabela_talhao = tabela_fazenda[tabela_talhao]

#Selecionar o Satélite 
filtro_satelite = st.sidebar.selectbox('🛰️ Selecione o Satélite:',('SENTINEL-2','Planet'))
tabela_satelite = tabela_talhao['Origem'] == filtro_satelite
tabela_satelite = tabela_talhao[tabela_satelite]

number =  st.sidebar.number_input('📶 Selecione o Grau da Regressão Polinomial:')

col1, col2 = st.columns(2)

# N° imagens Satelite
n_imagens= tabela_satelite.nunique()
n_planet = n_imagens["ID"]
col1.metric(label="📷 N° de Imagens:", value= n_planet)

#Média de imagens 
def numOfDays(date1, date2):
    return (date2-date1).days
     
date1 = tabela_satelite['Data'].iloc[0]
date1 = date1.split("/")
dia_date1=int(date1[0])
mes_date1=int(date1[1])
ano_date1=int(date1[2])
date1=date(ano_date1,mes_date1,dia_date1)

date2 = tabela_satelite['Data'].iloc[-1]
date2 = date2.split("/")
dia_date2=int(date2[0])
mes_date2=int(date2[1])
ano_date2=int(date2[2])
date2=date(ano_date2,mes_date2,dia_date2)

n_dias=numOfDays(date1, date2)
media_imagens = int(n_dias/n_planet)
col2.metric(label= "ℹ️ Resolução Temporal: ", value = media_imagens, delta = "dias",delta_color="off")


#Gráfico NDVI
st.title('Curva Fenológica NDVI')
fig = px.scatter(tabela_satelite, x='Data', y='Índice Médio NDVI', opacity=0.7)
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Índice Médio NDVI')
#Modelo Regressão
modelo = np.poly1d(np.polyfit(tabela_satelite['ID'], tabela_satelite['Índice Médio NDVI'],number))
y5 = modelo(tabela_satelite['ID'])
fig.add_traces(go.Scatter(x=tabela_satelite['Data'], y=y5, name="Regressão Polinomial"))

st.plotly_chart(fig)
    
  
#Gráfico NDRE
st.title('Curva Fenológica NDRE')
fig = px.scatter(tabela_satelite, x='Data', y='Índice Médio NDRE', opacity=0.7)
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Índice Médio NDRE')
#Modelo Regressão
modelo = np.poly1d(np.polyfit(tabela_satelite['ID'], tabela_satelite['Índice Médio NDRE'],number))
y5 = modelo(tabela_satelite['ID'])
fig.add_traces(go.Scatter(x=tabela_satelite['Data'], y=y5, name="Regressão Polinomial"))

st.plotly_chart(fig)  


# In[ ]:




