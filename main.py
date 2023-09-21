import streamlit as st
import pandas as pd
import plotly.express as px
import re
from despesas import get_despesas, mostrar_despesas
from graficos import calculate_total_by_coluna, grafico_barra_despesa

@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path, skiprows=4)
    return data

def get_subitens(data, selected_conta):
    # Obtém o número (xx) do valor selecionado
    selected_number = selected_conta.split(' ')[0]
    # Filtra os dados para incluir registros que começam com o mesmo número ou "FUxx"
    subitens = data[data['Conta'].str.startswith(selected_number) | data['Conta'].str.startswith(f'FU{selected_number}')]
    return subitens


def main():
    st.set_page_config(layout="wide")
    st.title('Análise de Seguridade Social')
    
    
    file_path = "FINBRA_Estados-DF_Despesas por Função_2018-2021.xlsx"
    
    if file_path is not None:
        data = load_data(file_path)
        
        st.subheader('Filtros')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            selected_uf = st.selectbox('Filtrar por UF', data['UF'].unique())

        with col2:
           coluna_options = ['Despesas Empenhadas', 'Despesas Liquidadas', 'Despesas Pagas']
           selected_coluna = st.selectbox('Filtrar por Coluna', coluna_options)

        with col3:
            selected_ano = st.selectbox('Filtrar por Ano', data['Ano'].unique())
        
        with col4:
            conta_options = ['08 - Assistência Social', '09 - Previdência Social','10 - Saúde']
            selected_conta = st.selectbox('Filtrar por Conta', conta_options)
  
        filtered_data = get_subitens(data, selected_conta)
        filtered_data = filtered_data[(filtered_data['UF'] == selected_uf) & (filtered_data['Coluna'] == selected_coluna) & (filtered_data['Ano'] == selected_ano)]

        st.subheader('Dados Filtrados')
        st.write(filtered_data)

        #Valores de Despesas
        despesas = get_despesas(data, selected_uf, selected_ano, selected_conta)
        mostrar_despesas(despesas, selected_uf, selected_ano)
        
        #Gráfico Despesa
        total_by_coluna = calculate_total_by_coluna(data, selected_uf, selected_ano, selected_conta)
        grafico_barra_despesa(total_by_coluna)
        
            
if __name__ == '__main__':
    main()
