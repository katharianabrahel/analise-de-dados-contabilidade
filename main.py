import streamlit as st
import pandas as pd
import plotly.express as px
import re


@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path, skiprows=4)
    return data


def calculate_total_by_coluna(data, selected_uf, selected_ano):
    filtered_data = data[(data['UF'] == selected_uf) & (data['Ano'] == selected_ano)]
    total_by_coluna = filtered_data.groupby('Coluna')['Valor (R$)'].sum().reset_index()
    return total_by_coluna


def get_subitens(data, selected_conta):
    # Obtém o número (xx) do valor selecionado
    selected_number = selected_conta.split(' ')[0]
    # Filtra os dados para incluir registros que começam com o mesmo número ou "FUxx"
    subitens = data[data['Conta'].str.startswith(selected_number) | data['Conta'].str.startswith(f'FU{selected_number}')]
    return subitens


def main():
    st.set_page_config(layout="wide")
    st.title('Análise de Despesas por Função 2018-2021')
    st.sidebar.title('Opções')
    

    file_path = st.sidebar.file_uploader('Carregar arquivo Excel (.xlsx)', type=['xlsx'])
    
    if file_path is not None:
        data = load_data(file_path)

        st.subheader('Dados brutos')
        st.write(data)

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

        total_by_coluna = calculate_total_by_coluna(data, selected_uf, selected_ano)

        st.subheader('Gráfico de Valor Total por Tipo de Despesa')
        fig = px.bar(total_by_coluna, x='Coluna', y='Valor (R$)', title=f'Valor Total por Tipo de Despesa em {selected_ano} ({selected_uf})')
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
