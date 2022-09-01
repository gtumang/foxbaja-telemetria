import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import time
import random
import datetime
import sys
import sqlite3
import os

velocidade=59
temp_cvt=34
combustivel=1

# def get_data_database():
#     ls_time = []
#     now = datetime.datetime.now()
#     for i in range(0,20):
#         now -= datetime.timedelta(seconds=1)
#         ls_time.append(now)
        
#     data = {
#         'velocidade': random.sample(range(0,40), 20),
#         'temperatura': random.sample(range(60,80), 20),
#         'tempo' : ls_time
#         }
#     df = pd.DataFrame(data=data)
#     return df

def get_data():
    if 'foxbaja_telemetria.db' not in os.listdir():
        print("\nERRO: base de dados nao existe\n")
        sys.exit()
    with sqlite3.connect('foxbaja_telemetria.db') as conn:
        c = conn.cursor()

        c.execute("""
            SELECT id, velocidade, temperatura, rotacao, timestamp FROM telemetria ORDER BY id DESC LIMIT 20
        """)
        rows = c.fetchall()
        # print(rows)
        df = pd.DataFrame(columns=['id', 'velocidade', 'temperatura', 'rotacao', 'timestamp'], data=rows)
        return df


df = get_data()

st.set_page_config(
    page_title="Dashboard Fox Baja",
    page_icon="🦊",
    layout="wide"
)


st.title('Dashboard Fox Baja')

placeholder = st.empty()


for i in range(200):

    df = get_data()

    with placeholder.container():
        st.columns(3)

        kpi1, kpi2, kpi3 = st.columns(3)

        # Velocidade:
        kpi1.metric(
            label="Velocidade",
            value=int(velocidade)
        )

        # Temperatura:
        kpi2.metric(
            label="Temperatura da CVT",
            value=int(temp_cvt)
        )

        # Gasolina:
        kpi3.metric(
            label="Nivel de combustivel",
            value=combustivel
        )



        fig_vel, fig_temp = st.columns(2)

        with fig_vel:
            st.markdown("### Histórico de Velocidade")
            fig = px.line(df, x="timestamp", y="velocidade")
            fig.update_layout(
            autosize=False,
            width=600,
            height=500)
            st.write(fig)

        with fig_temp:
            st.markdown('### Histórico de temperatura')
            fig2 = fig = px.line(df, x="timestamp", y="temperatura")
            fig2.update_layout(
            autosize=False,
            width=600,
            height=500)
            st.write(fig2)


        st.markdown("### Base completa")
        st.dataframe(df)
    time.sleep(1)





