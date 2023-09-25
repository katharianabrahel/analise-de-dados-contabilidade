import streamlit as st
import pandas as pd
import plotly.express as px
import re

def calculate_total_by_coluna(data, selected_uf, selected_ano, selected_conta):
    filtered_data = data.copy()
    
    if selected_uf != "Todas as UF":
        filtered_data = filtered_data[(filtered_data['UF'] == selected_uf)]
    if selected_ano != "Todos os Anos":
        filtered_data = filtered_data[(filtered_data['Ano'] == selected_ano)]
    if selected_conta != "Todas as Contas":
        filtered_data = filtered_data[(filtered_data['Conta'] == selected_conta)]    
    
    total_by_coluna = filtered_data.groupby('Coluna')['Valor (R$)'].sum().reset_index()
    
    return total_by_coluna

def grafico_barra_despesa(total_by_coluna):
    fig = px.bar(total_by_coluna, x='Status', y='Valor (R$)')
    st.plotly_chart(fig)