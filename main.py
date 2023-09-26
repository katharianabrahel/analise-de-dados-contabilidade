import streamlit as st
import pandas as pd
import plotly.express as px
import re
from despesas import get_despesas, mostrar_despesas
from graficos import calculate_total_by_coluna, grafico_barra_despesa, calculate_total_by_state_and_account, create_stacked_bar_chart


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


def formatar_valor(valor):
    try:
        valor = float(valor)
        if valor.is_integer():
            return "{:,.0f}".format(valor).replace(",", ".")
        else:
            return "{:,.2f}".format(valor).replace(",", "|").replace(".", ",").replace("|", ".")
    except ValueError:
        # Se não for um número, retorna o valor original.
        return valor


def main():
    st.set_page_config(layout="wide", page_title="Análise de Seguridade Social")
    st.sidebar.image('./images/logo-cin.png', use_column_width=True)
    st.title('Análise de Seguridade Social')
    
    
    file_path = "FINBRA_Estados-DF_Despesas por Função_2018-2021.xlsx"
    
    with st.sidebar:
        st.title("Funcionalidades")
        funcionalidades = st.selectbox('', ('Análise Detalhada por Estados', 'Análise Comparativa de Estados'))
    if file_path is not None:
        data = load_data(file_path)
        data.drop(columns=['Identificador da Conta', 'Cod.IBGE'], axis=1, inplace=True)
        data = data.query('Coluna in ["Despesas Empenhadas","Despesas Liquidadas","Despesas Pagas"]')
        
        if funcionalidades == 'Análise Detalhada por Estados':
            st.sidebar.subheader('Filtros')

            col1, col2, col3, col4 = st.columns(4)

            
            selected_uf = st.sidebar.selectbox('Filtrar por UF', ['Todas as UF'] + list(data['UF'].unique()))
                

            
            coluna_options = ['Todas as Colunas'] + ['Despesas Empenhadas', 'Despesas Liquidadas', 'Despesas Pagas']
            selected_coluna = st.sidebar.selectbox('Filtrar por Coluna', coluna_options)

           
            selected_ano = st.sidebar.selectbox('Filtrar por Ano', ['Todos os Anos'] + list(data['Ano'].unique()))

          
            conta_options = ['Todas as Contas'] + ['08 - Assistência Social', '09 - Previdência Social','10 - Saúde']
            selected_conta = st.sidebar.selectbox('Filtrar por Conta', conta_options)

            filtered_data = data.copy()
            data_visualization = data.copy()
            data_visualization = data_visualization.query('Conta in ["08 - Assistência Social","09 - Previdência Social","10 - Saúde"]')
            
            if selected_uf != "Todas as UF":
                filtered_data = filtered_data[(filtered_data['UF'] == selected_uf)]
                data_visualization = data_visualization[(data_visualization['UF'] == selected_uf)]
            if selected_coluna != "Todas as Colunas":
                filtered_data = filtered_data[(filtered_data['Coluna'] == selected_coluna)]
                data_visualization = data_visualization[(data_visualization['Coluna'] == selected_coluna)]
            if selected_ano != "Todos os Anos":
                filtered_data = filtered_data[(filtered_data['Ano'] == selected_ano)]
                data_visualization = data_visualization[(data_visualization['Ano'] == selected_ano)]
            if selected_conta != 'Todas as Contas':
                data_visualization = data_visualization[(data_visualization['Conta'] == selected_conta)]

            filtered_data = get_subitens(filtered_data, selected_conta)      
            
            st.subheader('Dados Filtrados')
            
            filtered_data_subfunctions = filtered_data.copy()
            # Aplica a função de formatação a todas as colunas numéricas.
            colunas_numericas = filtered_data.select_dtypes(include=['float64', 'int64']).columns
            filtered_data[colunas_numericas] = filtered_data[colunas_numericas].applymap(formatar_valor)
            data_visualization[colunas_numericas] = data_visualization[colunas_numericas].applymap(formatar_valor)

            toggle_state = st.checkbox("Visualizar subfunções")
            if toggle_state:
                st.write(filtered_data)
            else:
                st.write(data_visualization)

            #Valores de Despesas
            data = data.query('Conta in ["08 - Assistência Social","09 - Previdência Social","10 - Saúde"]')
            st.subheader(f'Valor Total por Estágio de Despesa ({selected_ano}, {selected_uf}, {selected_conta})')
            despesas = get_despesas(data, selected_uf, selected_ano, selected_conta)
            mostrar_despesas(despesas)
            
            #Gráfico Despesa
            with st.expander("Visualizar gráfico de despesa"):
                total_by_coluna = calculate_total_by_coluna(data, selected_uf, selected_ano, selected_conta)
                grafico_barra_despesa(total_by_coluna)
            
            #Gráfico Composição de Função

            st.subheader(f"Gráfico de Composição de Funções")
            
            if ((selected_uf != "Todas as UF") and (selected_conta != "Todas as Contas") and (selected_coluna != "Todas as Colunas") and (selected_ano != "Todos os Anos")):
                st.text(f"UF: {selected_uf} / Ano: {selected_ano} / Fase de Despesa: {selected_coluna} / Função: {selected_conta}")
                valores_subfuncoes = filtered_data_subfunctions['Valor (R$)'].tolist()
                nomes_subfuncoes = filtered_data_subfunctions['Conta'].tolist()
                indice = nomes_subfuncoes.index(selected_conta)
                valores_subfuncoes.pop(indice)
                nomes_subfuncoes.pop(indice)
                
                fig = px.pie(values=valores_subfuncoes, names=nomes_subfuncoes)
                st.plotly_chart(fig)
            else:
                st.warning('Você precisa especificar mais os critérios!', icon="⚠️")
        else:
            selected_year = st.sidebar.selectbox('Filtrar por Ano', ['Todos os Anos'] + list(data['Ano'].unique()))
            options = ['08 - Assistência Social', '09 - Previdência Social', '10 - Saúde']

            for selected_conta in options:
                
                if selected_year == 'Todos os Anos':
                    st.subheader(f'Somatório das Despesas por Estado para a Conta {selected_conta}')
                    filtered_data_year = data
                else:
                    st.subheader(f'Despesas por Estado para a Conta {selected_conta} em {selected_year}')
                    filtered_data_year = data[data['Ano'] == selected_year]
                
                # Calcula o somatório das despesas por estado e por tipo de conta
                total_by_state_account = calculate_total_by_state_and_account(filtered_data_year, selected_conta)

                # Cria o gráfico de barras empilhadas
                stacked_bar_chart = create_stacked_bar_chart(total_by_state_account, selected_conta)
                st.plotly_chart(stacked_bar_chart)

if __name__ == '__main__':
    main()
