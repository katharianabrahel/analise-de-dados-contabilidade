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
    if selected_conta == "Todas as Contas":
        # Se "Todas as Contas" estiver selecionada, retornar todos os itens e subitens da Conta.
        subitens = data[data['Conta'].str.startswith('08') | data['Conta'].str.startswith('09') | data['Conta'].str.startswith('10') | data['Conta'].str.startswith('FU08') | data['Conta'].str.startswith('FU09') | data['Conta'].str.startswith('FU10')]
    else:
        # Caso contrário, obtenha apenas os subitens relacionados à conta selecionada.
        selected_number = selected_conta.split(' ')[0]
        subitens = data[data['Conta'].str.startswith(selected_number) | data['Conta'].str.startswith(f'FU{selected_number}')]
    return subitens


def main():
    st.set_page_config(layout="wide")
    st.title('Análise de Seguridade Social')
    
    
    file_path = "FINBRA_Estados-DF_Despesas por Função_2018-2021.xlsx"
    
    if file_path is not None:
        data = load_data(file_path)
        data = data.query('Coluna in ["Despesas Empenhadas","Despesas Liquidadas","Despesas Pagas"]')
        st.subheader('Filtros')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            selected_uf = st.selectbox('Filtrar por UF', ['Todas as UF'] + list(data['UF'].unique()))

        with col2:
            coluna_options = ['Todas as Colunas'] + ['Despesas Empenhadas', 'Despesas Liquidadas', 'Despesas Pagas']
            selected_coluna = st.selectbox('Filtrar por Coluna', coluna_options)

        with col3:
            selected_ano = st.selectbox('Filtrar por Ano', ['Todos os Anos'] + list(data['Ano'].unique()))

        with col4:
            conta_options = ['Todas as Contas'] + ['08 - Assistência Social', '09 - Previdência Social','10 - Saúde']
            selected_conta = st.selectbox('Filtrar por Conta', conta_options)

        filtered_data = data.copy()
        
        if selected_uf != "Todas as UF":
            filtered_data = filtered_data[(filtered_data['UF'] == selected_uf)]
        if selected_coluna != "Todas as Colunas":
            filtered_data = filtered_data[(filtered_data['Coluna'] == selected_coluna)]
        if selected_ano != "Todos os Anos":
            filtered_data = filtered_data[(filtered_data['Ano'] == selected_ano)]
        #if selected_conta != "Todas as Contas":
        filtered_data = get_subitens(filtered_data, selected_conta)      
        
        st.subheader('Dados Filtrados')
        st.write(filtered_data)

        #Valores de Despesas
        data = data.query('Conta in ["08 - Assistência Social","09 - Previdência Social","10 - Saúde"]')
        st.subheader(f'Valor Total por Estágio de Despesa ({selected_ano}, {selected_uf}, {selected_conta})')
        despesas = get_despesas(data, selected_uf, selected_ano, selected_conta)
        mostrar_despesas(despesas)
        
        #Gráfico Despesa
        with st.expander("Visualizar gráfico de despesa"):
            total_by_coluna = calculate_total_by_coluna(data, selected_uf, selected_ano, selected_conta)
            grafico_barra_despesa(total_by_coluna)
        
            
if __name__ == '__main__':
    main()
