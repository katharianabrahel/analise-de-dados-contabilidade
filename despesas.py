import streamlit as st
import pandas as pd
import plotly.express as px
import re

def formatar_numero(numero):
    """
    Função responsável por colocar sufixo nos números baseados na escala númerica.
    """
    sufixos_singular = ['', ' mil', ' milhão', ' bilhão', ' trilhão']
    sufixos_plural = ['', ' mil', ' milhões', ' bilhões', ' trilhões']

    escala = 0
    while numero >= 1000 and escala < len(sufixos_singular) - 1:
        escala += 1
        numero /= 1000.0
    
    numero_formatado = f'{numero:.2f}'
    
    numero_formatado = numero_formatado.rstrip('0').rstrip('.')
    
    comparacao = numero_formatado.split('.')
    if comparacao[0] == '1':
        numero_formatado += sufixos_singular[escala]
    else:
        numero_formatado += sufixos_plural[escala]
    
    return numero_formatado

def decimal_para_porcentagem(numero):
    """
    Função responsável por converter números na escala de 0 a 1 em porcentagem
    """
    if numero <= 1:
        porcentagem = numero * 100
    else:
        porcentagem = 100
    return f'{porcentagem:.2f}%'


def get_despesas(data, selected_uf, selected_ano, selected_conta):
    """
    Função responsável por entregar as despesas empenhadas, liquidadas e pagas.
    Os parâmetros para filtrar as despesas são: UF, ANO e CONTA
    """
    
    filtered_data = data.copy()

    if selected_uf != "Todas as UF":
        filtered_data = filtered_data[(filtered_data['UF'] == selected_uf)]
    if selected_ano != "Todos os Anos":
        filtered_data = filtered_data[(filtered_data['Ano'] == selected_ano)]
    if selected_conta != "Todas as Contas":
        filtered_data = filtered_data[(filtered_data['Conta'] == selected_conta)]    
    
    despesas_empenhadas = filtered_data[filtered_data['Coluna'] == 'Despesas Empenhadas']['Valor (R$)'].sum()
    despesas_liquidadas = filtered_data[filtered_data['Coluna'] == 'Despesas Liquidadas']['Valor (R$)'].sum()
    despesas_pagas = filtered_data[filtered_data['Coluna'] == 'Despesas Pagas']['Valor (R$)'].sum()

    return [despesas_empenhadas, despesas_liquidadas, despesas_pagas]


def mostrar_despesas(despesas):
    """
    Função responsável por colocar visualmente as despesas no Streamlit.
    Os dados colocados são: Despesas Empenhadas, Despesas Liquidadas, Despesas Pagas, Execução de Despesa.
    """
    col5, col6, col7, col8 = st.columns(4) 
    col5.metric("Despesas Empenhadas", formatar_numero(despesas[0]))
    col6.metric("Despesas Liquidadas", formatar_numero(despesas[1]))
    col7.metric("Despesas Pagas", formatar_numero(despesas[2]))
    col8.metric("Taxa de Execução", decimal_para_porcentagem(despesas[2]/despesas[0]))