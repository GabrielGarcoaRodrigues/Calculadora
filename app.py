import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import matplotlib.pyplot as plt
from vega_datasets import data
import random

st.set_page_config(page_title='Calculadora Gestão de Crises', page_icon='<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M320-320v50q0 13 8.5 21.5T350-240q13 0 21.5-8.5T380-270v-50h50q13 0 21.5-8.5T460-350q0-13-8.5-21.5T430-380h-50v-50q0-13-8.5-21.5T350-460q-13 0-21.5 8.5T320-430v50h-50q-13 0-21.5 8.5T240-350q0 13 8.5 21.5T270-320h50Zm230 50h140q13 0 21.5-8.5T720-300q0-13-8.5-21.5T690-330H550q-13 0-21.5 8.5T520-300q0 13 8.5 21.5T550-270Zm0-100h140q13 0 21.5-8.5T720-400q0-13-8.5-21.5T690-430H550q-13 0-21.5 8.5T520-400q0 13 8.5 21.5T550-370Zm70-208 35 35q9 9 21 9t21-9q8-8 8.5-20.5T698-585l-36-37 35-35q9-9 9-21t-9-21q-9-9-21-9t-21 9l-35 35-35-35q-9-9-21-9t-21 9q-9 9-9 21t9 21l35 35-36 37q-8 9-8 21t9 21q9 9 21 9t21-9l35-35Zm-340-14h140q13 0 21.5-8.5T450-622q0-13-8.5-21.5T420-652H280q-13 0-21.5 8.5T250-622q0 13 8.5 21.5T280-592Zm-80 472q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>', layout='wide')

# Carregar o arquivo Excel
file_path = os.path.join(os.path.dirname(__file__), 'arquivo.xlsx')
df = pd.read_excel(file_path, sheet_name='Atualizada')

if 'Teste' in df['Marca'].values:
  df.drop(df[df['Marca'] == 'Teste'].index)




st.markdown(
    """
    <style>
    .body{
        height:500px
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Calculadora Gestão de Crises :chart_with_downwards_trend:", divider="blue")

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)


with st.form(key='my_form'):
    with col1:
        sensibilidade_input = st.selectbox('Sensibilidade',
                                           [
                                               'Muito Baixa',
                                               'Baixa',
                                               'Média',
                                               'Alta',
                                               'Muito Alta'
                                           ])
    switcher = {
        'Muito Baixa': 0,
        'Baixa': 15,
        'Média': 30,
        'Alta': 45,
        'Muito Alta': 60
    }
    sensibilidade = switcher.get(sensibilidade_input, 0)

    switcher = {
          'Muito Baixa': 1,
          'Baixa': 2,
          'Média': 3,
          'Alta': 4,
          'Muito Alta': 5
    }
    sensibilidade_int = switcher.get(sensibilidade_input, 0)

    switcher = {
        'Muito Baixa': 20,
        'Baixa': 40,
        'Média': 60,
        'Alta': 80,
        'Muito Alta': 100
    }
    sensibilidade_porcentagem = switcher.get(sensibilidade_input, 0)

    with col2:
        protagonismo = st.selectbox('Protagonismo',
                                    [
                                        'Figurante',
                                        'Coadjuvante',
                                        'Protagonista indireto',
                                        'Protagonista'
                                    ])
        switcher = {
            'Figurante': 10,
            'Coadjuvante': 20,
            'Protagonista indireto': 30,
            'Protagonista': 40
        }
        protagonismo = switcher.get(protagonismo, 0)

    with col3:
        volumetria = st.number_input(
            'Volumetria', value=0, format="%d", step=1, min_value=0)
        intervalos = {
            (0, 4168): 0,
            (4169, 19359): 5,
            (19360, 30189): 10,
            (30190, 44791): 15,
            (44792, float('inf')): 20
        }

        # Função para encontrar o intervalo correto
        volumetria = next(value for (
            start, end), value in intervalos.items() if start <= volumetria <= end)

    with col4:
        usuarios_unicos = st.number_input(
            'Usuários Únicos', value=0, format="%d", step=1, min_value=0)
        intervalos = {
            (0, 3084): 0,
            (3085, 14325): 5,
            (14326, 22339): 10,
            (22340, 33145): 15,
            (33146, float('inf')): 20
        }

        # Função para encontrar o intervalo correto
        usuarios_unicos = next(value for (
            start, end), value in intervalos.items() if start <= usuarios_unicos <= end)

    with col5:
        tempo_reverberacao_input = st.number_input(
            'Tempo de Reverberação', value=0, format="%d",  step=1, min_value=0)
        intervalos = {
            (0, 2): 0,
            (3, 3): 5,
            (4, 6): 10,
            (7, 12): 15,
            (13, float('inf')): 20
        }

        tempo_reverberacao = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao_input <= end)
        
        intervalos = {
            (0, 2): 20,
            (3, 3): 40,
            (4, 6): 60,
            (7, 12): 80,
            (13, float('inf')): 100
        }
        tempo_porcentagem = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao_input <= end)

    with col6:
        saude_input = st.number_input(
            'Saúde (%)', value=0, format="%d",  step=1, max_value=100, min_value=0)
        intervalos = {
            (0, 50): 0,
            (51, 60): -10,
            (61, 70): -20,
            (71, 80): -30,
            (81, 100): -40
        }
        saude_ajustado = next(value for (
            start, end), value in intervalos.items() if start <= saude_input <= end)

    with col7:
        veiculos_idm = st.number_input(
            'Veiculos IDM', value=0, format="%d", step=1, min_value=0)
        intervalos = {
            (0, 6): 0,
            (7, 16): 5,
            (17, 24): 10,
            (25, 33): 15,
            (34, float('inf')): 20
        }
        veiculos_idm = next(value for (
            start, end), value in intervalos.items() if start <= veiculos_idm <= end)

    with col8:
        veiculos_nao_idm = st.number_input(
            'Veiculos Não-IDM', value=0, format="%d",  step=1, min_value=0)
        intervalos = {
            (0, 5): 0,
            (6, 14): 5,
            (15, 20): 10,
            (21, 25): 15,
            (26, float('inf')): 20
        }
        veiculos_nao_idm = next(value for (
            start, end), value in intervalos.items() if start <= veiculos_nao_idm <= end)


soma = (sensibilidade + protagonismo + volumetria + usuarios_unicos +
        tempo_reverberacao + saude_ajustado + veiculos_idm + veiculos_nao_idm)
intervalos = {
    (-100, 20): "Monitorar",
    (21, 40): "Incidente P",
    (41, 60): "Incidente M",
    (61, 80): "Incidente G",
    (81, 100): "Incidente GG",
    (101, 120): "Crise PP",
    (121, 140): "Crise P",
    (141, 160): "Crise M",
    (161, 180): "Crise G",
    (181, float("inf")): "Crise GG",
}
soma = next(value for (start, end), value in intervalos.items()
            if start <= soma <= end)

switcher = {
    "Monitorar": "#32CD32",
    "Incidente P": "#fbd6a1",
    "Incidente M": "#f9c8cc",
    "Incidente G": "#f7ba76",
    "Incidente GG": "#f29f60",
    "Crise PP": "#e97748",
    "Crise P": "#df5030",
    "Crise M": "#d62818",
    "Crise G": "red",
    "Crise GG": "#8a0000",
}
background_color = switcher.get(soma, 0)

# Adiciona uma linha
df.loc[len(df)] = ['Teste', sensibilidade_int, 'Teste', soma, 1, 'Teste', tempo_reverberacao_input, volumetria, saude_input/100, random.random()]


# Média de Saúde e Tempo de duração da crise
saude_media = (df['Saúde'].mean() * 100)
media_tempo_reverberacao = df['Tempo de duração da crise (em dias)'].mean()


st.html(
    f'<div style="display:flex;margin:0 auto;margin-top:20px;background-color:{background_color}"><h1 style="display:block;margin:0 auto;text-align:center;font-weight:bold;text-shadow: #000 2px 3px 2px;">{soma}</h1></div>')

# HTML e CSS formatado para Streamlit
html_code = f"""
<head>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300i,400" rel="stylesheet">
  <style>
    body {{
      background-color: #100e17;
      font-family: 'Open Sans', sans-serif;
    }}

    .container {{
      margin: 0 auto;
      height: 450px;
      width: 1000px;
      top: 60px;
      left: calc(50% - 400px);
      display: flex;
    }}

    .card {{
      display: flex;
      height: 300px;
      width: 400px;
      background-color: #17141d;
      border-radius: 10px;
      box-shadow: -1rem 0 3rem #000;
      transition: 0.4s ease-out;
      position: relative;
      left: 0px;
      top:15%;
    }}

    .card:not(:first-child) {{
        margin-left: -50px;
    }}

    .card:hover {{
      transform: translateY(-20px);
      transition: 0.4s ease-out;
    }}

    .card:hover ~ .card {{
      position: relative;
      left: 50px;
      transition: 0.4s ease-out;
    }}

    .title {{
      color: white;
      font-weight: 300;
      position: absolute;
      left: 20px;
      top: 15px;
    }}

    .bar {{
      position: absolute;
      top: 100px;
      left: 30px;
      height: 5px;
      width: 290px;
    }}

    .emptybar {{
      background-color: #2e3033;
      width: 100%;
      height: 100%;
    }}

    .filledbar_saude, .filledbar_tempo, .filledbar_sensibilidade {{
      position: absolute;
      top: 0px;
      z-index: 3;
      width: 0px;
      height: 100%;
      background: rgb(0,154,217);
      background: linear-gradient(90deg, rgba(0,154,217,1) 0%, rgba(217,147,0,1) 65%, rgba(255,186,0,1) 100%);
      transition: 0.6s ease-out;
    }}

    .card:hover .filledbar_saude {{
      width: {saude_input}%;
      transition: 0.4s ease-out;
    }}

    .card:hover .filledbar_tempo {{
      width: {tempo_porcentagem}%;
      transition: 0.4s ease-out;
    }}

    .card:hover .filledbar_sensibilidade {{
      width: {sensibilidade_porcentagem}%;
      transition: 0.4s ease-out;
    }}

    .circle {{
      position: absolute;
      top: 150px;
      left: calc(48% - 25px);
    }}

    .circle2 {{
      position: absolute;
      top: 150px;
      width: 150px;
      left: calc(29%);
      text-align: center;
    }}

    .stroke {{
      stroke: white;
      stroke-dasharray: 360;
      stroke-dashoffset: 360;
      transition: 0.6s ease-out;
    }}

    svg {{
      fill: #17141d;
      stroke-width: 2px;
    }}

    .card:hover .stroke {{
      stroke-dashoffset: 100;
      transition: 0.6s ease-out;
    }}

    /* Centraliza o texto dentro do círculo */
    .circle text, .circle2 text {{
      fill: white;
      font-size: 29px;
      text-anchor: middle;
      font-weight:Bold;
      dominant-baseline: central;
    }}

    .descript{{
      text-align: center;
      position: absolute;
      top: 215px;
      width:300px;
      left: calc(8%);
    }}

    .descript_rever{{
      text-align: center;
      position: absolute;
      top: 215px;
      width:210px;
      left: calc(23%);
    }}

  </style>
</head>
<body class="body">
<div class="container">
  <div class="card">
    <h3 class="title">Saúde</h3>
    <div class="bar">
      <div class="emptybar"></div>
      <div class="filledbar_saude"></div>
    </div>
    <div class="circle">
      <text x="60" y="60">{saude_input}%</text>
    </div>
    <text class="descript">A saúde média é de {saude_media:.2f}%</text>
  </div>
  <div class="card">
    <h3 class="title">Tempo de Reverberação</h3>
    <div class="bar">
      <div class="emptybar"></div>
      <div class="filledbar_tempo"></div>
    </div>
    <div class="circle">
        <text x="60" y="60">{tempo_reverberacao_input} dias</text>
    </div>
    <text class="descript_rever">O tempo médio de reverberação é de {media_tempo_reverberacao:.2f} dias</text>
  </div>
  <div class="card">
    <h3 class="title">Sensibilidade</h3>
    <div class="bar">
      <div class="emptybar"></div>
      <div class="filledbar_sensibilidade"></div>
    </div>
    <div class="circle2">
      <text x="60" y="60">{sensibilidade_input}</text>
    </div>
    <text class="descript">A sensibilidade mais comum é 'Muito Alta'</text>
  </div>
</div>
</body>
"""



st.markdown(html_code, unsafe_allow_html=True)






# Cria o gráfico Altair
base = alt.Chart(df).mark_circle(size=180).encode(
    alt.X('Saúde', scale=alt.Scale(domain=(-0.02, 1.02)), title='Menos Saúde  ⭠  Porcentagem de Saúde  ⭢  Mais Saúde',
          axis=alt.Axis(tickCount=10, format='%', titleFont='Open Sans', titleFontSize=13, titleColor='white')),
    alt.Y('Random',  title='', axis=alt.Axis(
          tickCount=6, format='d', titleFont='Arial', titleFontSize=13, titleColor='white')),
    color=alt.Color('Marca'),
    size=alt.Size('Tamanho', scale=alt.Scale(range=[300, 2000]), sort=['Possível Crise', 'P', 'M', 'G', 'GG'], legend=alt.Legend(
        title="Tamanho",  # Título da legenda
        titleColor="White",  # Cor do título da legenda
        labelColor="White",  # Cor dos rótulos da legenda
        symbolType="circle",
        symbolFillColor="White",
    )),
    tooltip=['Marca', 'Tema', 'Tamanho', 'Saúde', 'Sensibilidade']

).properties(
    width=500,  # Largura do gráfico
    height=600  # Altura do gráfico
)
# Exibe o gráfico no Streamlit
st.altair_chart(base, use_container_width=True)


# Gráfico de barras

# Mapeie os valores de sensibilidade para rótulos
sensitivity_mapping = {1: 'Muito Baixa', 2: 'Baixa',
                       3: 'Média', 4: 'Alta', 5: 'Muito Alta'}
df['Sensibilidade Label'] = df['Sensibilidade'].map(sensitivity_mapping)

base = alt.Chart(df).encode(
    alt.X('count(Sensibilidade)', title='Quantidade'),
    alt.Y('Sensibilidade Label', title='Sensibilidade', axis=alt.Axis(labelFontSize=16), sort=[
          'Muito Alta', 'Alta', 'Média', 'Baixa', 'Muito Baixa'])  # Ordenando os rótulos
).properties(
    width=650,  # Largura do gráfico
    height=450  # Altura do gráfico
)

# Gráfico de barras com labels de somatório no final de cada barra
chart = base.mark_bar(size=35).encode(
    text=alt.Text('count(Sensibilidade):Q')
).mark_text(
    align='left',
    baseline='middle',
    dx=3,  # deslocamento do texto em relação ao final da barra
    color='white',
    fontWeight='bold',
    fontSize=15
)

# Combinação do gráfico de barras com os textos
final_chart = base.mark_bar(size=35) + chart

# Exiba o gráfico
final_chart



# Renderizar o HTML no Streamlit
st.button("Adicionar crise ao histórico")
