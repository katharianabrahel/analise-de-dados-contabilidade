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
    fig = px.bar(total_by_coluna, x='Coluna', y='Valor (R$)')
    st.plotly_chart(fig)

def calculate_total_by_state_and_account(data, account):
    total_by_state = data[data['Conta'] == account].groupby(['UF', 'Coluna'])['Valor (R$)'].sum().reset_index()
    return total_by_state


def create_stacked_bar_chart(data, account):
    fig = px.bar(data, x='UF', y='Valor (R$)', color='Coluna', barmode='group')
    fig.update_layout(xaxis_title='Estado', yaxis_title='Valor (R$)', width=1200, height=600)
    return fig