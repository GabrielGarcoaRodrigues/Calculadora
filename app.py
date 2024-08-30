import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import random
from streamlit_modal import Modal
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title='Calculadora Gestão de Crises', page_icon='<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M320-320v50q0 13 8.5 21.5T350-240q13 0 21.5-8.5T380-270v-50h50q13 0 21.5-8.5T460-350q0-13-8.5-21.5T430-380h-50v-50q0-13-8.5-21.5T350-460q-13 0-21.5 8.5T320-430v50h-50q-13 0-21.5 8.5T240-350q0 13 8.5 21.5T270-320h50Zm230 50h140q13 0 21.5-8.5T720-300q0-13-8.5-21.5T690-330H550q-13 0-21.5 8.5T520-300q0 13 8.5 21.5T550-270Zm0-100h140q13 0 21.5-8.5T720-400q0-13-8.5-21.5T690-430H550q-13 0-21.5 8.5T520-400q0 13 8.5 21.5T550-370Zm70-208 35 35q9 9 21 9t21-9q8-8 8.5-20.5T698-585l-36-37 35-35q9-9 9-21t-9-21q-9-9-21-9t-21 9l-35 35-35-35q-9-9-21-9t-21 9q-9 9-9 21t9 21l35 35-36 37q-8 9-8 21t9 21q9 9 21 9t21-9l35-35Zm-340-14h140q13 0 21.5-8.5T450-622q0-13-8.5-21.5T420-652H280q-13 0-21.5 8.5T250-622q0 13 8.5 21.5T280-592Zm-80 472q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-80h560v-560H200v560Zm0-560v560-560Z"/></svg>', layout='wide')
# Injetar CSS customizado para mudar a cor do fundo da página
st.markdown(
    """
    <style>
    .st-emotion-cache-13k62yr {
        background-color: #262626;
    }
    .st-emotion-cache-h4xjwg {
        background-color: #262626;
    }
    </style>
    """,
    unsafe_allow_html=True
)


json_path = os.path.join(os.path.dirname(__file__), 'arquivo.json')
# Configurar o acesso à API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

# Acessar a planilha e a aba específica
sheet = client.open("Gestão de crises - Tableau").worksheet('Atualizada')  # ou use .worksheet("Nome da aba")

# Carregar os dados em um DataFrame do pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)


if 'CRISE EM ANALISE' in df['Marca'].values:
    df.drop(df[df['Marca'] == 'CRISE EM ANALISE'].index)

color_dict = {
    'Ambev': '#2e008b',  
    'Ambev Tech': '#F7C300', 
    'Beats': '#005CB9', 
    'Bees Bank': '#A6192E',
    'Brahma': '#FF0000',  
    'Budweiser': '#C8102E',
    'CRISE EM ANALISE': 'white',  
    'Fusion': '#00FF00',  
    'Guaraná': '#4CAF50',  
    'Michelob': '#002868',  
    'Mikes': '#FFA500',  
    'Skol': '#FFD700',  
    'Spaten': '#046A38',  
    'Zé Delivery': '#FFCC00',  
}



st.header("Calculadora Gestão de Crises :chart_with_downwards_trend:", divider="blue")

col1, col2 = st.columns([1, 4])

with col1:
    sensibilidade_input = st.selectbox('Sensibilidade',
                                       ['Muito Baixa', 'Baixa', 'Média', 'Alta', 'Muito Alta'])
    switcher = {'Muito Baixa': 0, 'Baixa': 15, 'Média': 30, 'Alta': 45, 'Muito Alta': 60}
    sensibilidade = switcher.get(sensibilidade_input, 0)

    switcher = {'Muito Baixa': 1, 'Baixa': 2, 'Média': 3, 'Alta': 4, 'Muito Alta': 5}
    sensibilidade_int = switcher.get(sensibilidade_input, 0)

    switcher = {'Muito Baixa': 20, 'Baixa': 40, 'Média': 60, 'Alta': 80, 'Muito Alta': 100}
    sensibilidade_porcentagem = switcher.get(sensibilidade_input, 0)

    protagonismo = st.selectbox('Protagonismo', ['Figurante', 'Coadjuvante', 'Protagonista indireto', 'Protagonista'])
    switcher = {'Figurante': 10, 'Coadjuvante': 20, 'Protagonista indireto': 30, 'Protagonista': 40}
    protagonismo = switcher.get(protagonismo, 0)

    volumetria_input = st.number_input('Volumetria', value=0, format="%d", step=1, min_value=0)
    intervalos = {(0, 4168): 0, (4169, 19359): 5, (19360, 30189): 10, (30190, 44791): 15, (44792, float('inf')): 20}
    volumetria = next(value for (start, end), value in intervalos.items() if start <= volumetria_input <= end)

    usuarios_unicos_input = st.number_input('Usuários Únicos', value=0, format="%d", step=1, min_value=0)
    intervalos = {(0, 3084): 0, (3085, 14325): 5, (14326, 22339): 10, (22340, 33145): 15, (33146, float('inf')): 20}
    usuarios_unicos = next(value for (start, end), value in intervalos.items() if start <= usuarios_unicos_input <= end)

    tempo_reverberacao_input = st.number_input('Tempo de Reverberação', value=0, format="%d", step=1, min_value=0)
    intervalos = {(0, 2): 0, (3, 3): 5, (4, 6): 10, (7, 12): 15, (13, float('inf')): 20}
    tempo_reverberacao = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao_input <= end)
    
    intervalos = {(0, 2): 20, (3, 3): 40, (4, 6): 60, (7, 12): 80, (13, float('inf')): 100}
    tempo_porcentagem = next(value for (start, end), value in intervalos.items() if start <= tempo_reverberacao_input <= end)

    saude_input = st.number_input('Saúde (%)', value=0, format="%d", step=1, max_value=100, min_value=0)
    intervalos = {(0, 50): 0, (51, 60): -10, (61, 70): -20, (71, 80): -30, (81, 100): -40}
    saude_ajustado = next(value for (start, end), value in intervalos.items() if start <= saude_input <= end)

    veiculos_idm_input = st.number_input('Veiculos IDM', value=0, format="%d", step=1, min_value=0)
    intervalos = {(0, 6): 0, (7, 16): 5, (17, 24): 10, (25, 33): 15, (34, float('inf')): 20}
    veiculos_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_idm_input <= end)

    veiculos_nao_idm_input = st.number_input('Veiculos Não-IDM', value=0, format="%d", step=1, min_value=0)
    intervalos = {(0, 5): 0, (6, 14): 5, (15, 20): 10, (21, 25): 15, (26, float('inf')): 20}
    veiculos_nao_idm = next(value for (start, end), value in intervalos.items() if start <= veiculos_nao_idm_input <= end)

    st.button("Adicionar Crise ao Histórico", use_container_width=True)
    # if st.button("Adicionar Crise ao Histórico", use_container_width=True):
        # with st.expander("", expanded=True):
        #     with st.form(key='form'):
        #         marca = st.text_input('Marca')
        #         tema = st.text_input('Tema')
        #         ano = st.number_input('Ano', value=2024, format="%d", step=1, min_value=2022)
        #         mes = st.selectbox('Mês', ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'])
        #         st.form_submit_button("Salvar", use_container_width=True)




    soma = (sensibilidade + protagonismo + volumetria + usuarios_unicos + tempo_reverberacao + saude_ajustado + veiculos_idm + veiculos_nao_idm)
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
    resultado = next(value for (start, end), value in intervalos.items() if start <= soma <= end)

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
    background_color = switcher.get(resultado, 0)

    # Adiciona uma linha
    df.loc[len(df)] = ['CRISE EM ANÁLISE', sensibilidade_int, 'CRISE EM ANÁLISE', 'CRISE EM ANÁLISE', 2024, 'CRISE EM ANÁLISE', tempo_reverberacao_input, volumetria_input, f'{saude_input:.2f}%', random.random()]
    # Remover o símbolo de porcentagem, substituir a vírgula por ponto, e converter para float
    df['Saúde'] = df['Saúde'].str.replace('%', '').str.replace(',', '.').astype(float)

    # Dividir por 100 para que os valores estejam entre 0 e 1
    df['Saúde'] = df['Saúde'] / 100

    dict_sensibilidade = {
        1: 'Muito Baixa',
        2: 'Baixa',
        3: 'Média',
        4: 'Alta',
        5: 'Muito Alta'
    }

    df['Sensibilidade'] = df['Sensibilidade'].map(dict_sensibilidade)
    

    def sensibilidade_random(sensibilidade):
        if sensibilidade == 'Muito Baixa':
            return random.uniform(0, 0.4)
        elif sensibilidade == 'Baixa':
            return random.uniform(0.6, 1.0)
        elif sensibilidade == 'Média':
            return random.uniform(1.2, 1.6)
        elif sensibilidade == 'Alta':
            return random.uniform(1.8, 2.2)
        else:
            return random.uniform(2.4, 3.3)

# Aplica a função a cada linha da coluna 'Sensibilidade'
    df['Sensibilidade_random'] = df['Sensibilidade'].apply(sensibilidade_random)


with col2:
    st.html(f'<div style="display:flex;margin:0 auto;background-color:{background_color}"><h1 style="display:block;margin:0 auto;text-align:center;font-weight:bold;text-shadow: #000 2px 3px 2px;font-size:36px;">{resultado}</h1></div>')
    # Cria o gráfico Altair
    base = alt.Chart(df).mark_circle(size=180).encode(
        alt.X('Saúde', scale=alt.Scale(domain=[0.0,1.0]),  title='Menos Saúde  ⭠  Porcentagem de Saúde  ⭢  Mais Saúde',
            axis=alt.Axis(tickCount=10, format='%', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor='white')),
        alt.Y('Sensibilidade_random',  title='Menor Sensibilidade  ⭠  Sensibilidade  ⭢  Maior Sensibilidade', axis=alt.Axis(
            tickCount=15, format='d', titleFont='Arial', titleFontSize=14, titleColor='white', gridColor=None, labelColor='#262626')),
        color=alt.condition(
            alt.datum.Marca == 'CRISE EM ANÁLISE',
            alt.value('white'),  # Cor da bolha para "Crise em Análise"
            alt.Color('Marca', scale=alt.Scale(domain=list(color_dict.keys()), range=list(color_dict.values())), legend=alt.Legend(
                title="Marca",
                titleColor="White",
                labelColor="White",
                symbolType="circle",
                symbolFillColor="White",
                orient='right',
            ))
        ),
        size=alt.Size('Tamanho', scale=alt.Scale(range=[300, 2500]), sort=['Incidente P', 'Incidente M', 'Incidente G', 'Incidente GG', 'Possível Crise','PP', 'P', 'M', 'G', 'GG'], legend=alt.Legend(
            title="Tamanho",
            titleColor="White",
            labelColor="White",
            symbolType="circle",
            symbolFillColor="White",
            orient='right',
            offset=50  # Ajuste a distância para ficar abaixo da legenda de Marca
        )),
        stroke=alt.condition(
            alt.datum.Marca == 'CRISE EM ANÁLISE',
            alt.value('white'),  # Cor da borda para "Crise em Análise"
            alt.value('transparent')  # Sem borda para outras crises
        ),
        strokeWidth=alt.condition(
            alt.datum.Marca == 'CRISE EM ANÁLISE',
            alt.value(3),  # Espessura da borda para "Crise em Análise"
            alt.value(0)  # Sem borda para outras crises
        ),
        tooltip=[
            alt.Tooltip('Marca'),
            alt.Tooltip('Tema'),
            alt.Tooltip('Tamanho'),
            alt.Tooltip('Saúde', format='.0%'),  # Formata o valor da Saúde como número inteiro
            alt.Tooltip('Sensibilidade')
            ]
).properties(
        width=500,  # Largura do gráfico
        height=700,  # Altura do gráfico
        background='#262626',  # Cor de fundo do gráfico
    )
    # Exibe o gráfico no Streamlit
    st.altair_chart(base, use_container_width=True)
