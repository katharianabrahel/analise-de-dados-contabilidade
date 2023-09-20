import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path, skiprows=4)
    return data


def calculate_total_by_coluna(data, selected_uf, selected_ano):
    filtered_data = data[(data['UF'] == selected_uf) & (data['Ano'] == selected_ano)]
    total_by_coluna = filtered_data.groupby('Coluna')['Valor (R$)'].sum().reset_index()
    return total_by_coluna


def main():
    st.title('Análise de Despesas por Função 2018-2021')
    st.sidebar.title('Opções')
    

    # Carregue os dados
    file_path = st.sidebar.file_uploader('Carregar arquivo Excel (.xlsx)', type=['xlsx'])
    
    if file_path is not None:
        data = load_data(file_path)

        st.subheader('Dados brutos')
        st.write(data)

        st.subheader('Filtros')

        selected_uf = st.selectbox('Filtrar por UF', data['UF'].unique())
        selected_coluna = st.selectbox('Filtrar por Coluna', data['Coluna'].unique())
        selected_ano = st.selectbox('Filtrar por Ano', data['Ano'].unique())

        filtered_data = data[(data['UF'] == selected_uf) & (data['Coluna'] == selected_coluna) & (data['Ano'] == selected_ano)] 

        st.subheader('Dados Filtrados')
        st.write(filtered_data)

        # Calcule a soma dos valores por tipo de despesa (Coluna)
        total_by_coluna = calculate_total_by_coluna(data, selected_uf, selected_ano)

        st.subheader('Gráfico de Valor Total por Tipo de Despesa')
        fig = px.bar(total_by_coluna, x='Coluna', y='Valor (R$)', title=f'Valor Total por Tipo de Despesa em {selected_ano} ({selected_uf})')
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
