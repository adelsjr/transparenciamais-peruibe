import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# --- Configuração da Página ---
st.set_page_config(page_title="Transparência Mais Peruíbe", layout="wide", page_icon="🎯")

# --- CONTEÚDO PRINCIPAL DO DASHBOARD ---
st.title("Transparência Mais Peruíbe")
st.warning("Projeto ainda em construção...", icon="🚧")
# Frase de missão
st.markdown("""
O objetivo deste **portal independente** é levar mais transparência ao orçamento da cidade de Peruíbe. Para que seus cidadãos possam **entender**, **fiscalizar** e **cobrar** o poder público.
""")

# Aviso/Disclaimer em caixa de cor
st.info("Esse portal cruza os dados da [LOA (Lei Orçamentária Anual)](http://leismunicipa.is/0yb2x) com as despesas publicadas no Portal da Transparência da cidade.")

st.markdown("---")

# Link para as explicações no menu lateral
st.markdown("Saiba como ler estas informações clicando no menu lateral")

# --- FUNÇÃO PARA COLORIR A TABELA ---
def color_estouro_percent(val):
    if val > 5.0:
        return 'background-color: #ffcccb'
    elif val > 0 and val <= 5.0:
        return 'background-color: #ffffcc'
    else:
        return 'background-color: #c4f7c4'

# --- Carregamento e Tratamento dos Dados ---
@st.cache_data
def carregar_dados_executados(ano):
    caminho_dados = f'dados_limpos/despesas_limpo_{ano}.csv'
    try:
        df = pd.read_csv(caminho_dados, delimiter=';', decimal=',')
        cols_monetarias = ['Empenhado', 'Anulado', 'Liquidado', 'Pago', 'Saldo']
        for col in cols_monetarias:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{caminho_dados}' não encontrado.")
        return pd.DataFrame()

@st.cache_data
def carregar_dados_loa_orgaos():
    caminho = 'loa_por_orgaos.csv'
    try:
        df_loa = pd.read_csv(caminho)
        df_loa['Valor'] = df_loa['Valor'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
        df_loa['Codigo'] = df_loa['Codigo'].str.extract(r'^\s*(\d{2}\.\d{2}\.\d{2})')
        return df_loa
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{caminho}' não encontrado.")
        return pd.DataFrame()

@st.cache_data
def carregar_mapeamento():
    caminho = 'mapeamento_orgaos.csv'
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{caminho}' não encontrado. Por favor, execute 'gerar_mapeamento.py' primeiro.")
        return pd.DataFrame()

# Carregamento dos dados
df_executado = carregar_dados_executados("2024")
df_loa_orgaos = carregar_dados_loa_orgaos()
df_mapeamento = carregar_mapeamento()

if not df_executado.empty and not df_loa_orgaos.empty and not df_mapeamento.empty:
    # 1. Aplicar o mapeamento para padronizar os nomes dos órgãos
    mapeamento_dict = df_mapeamento.set_index('Unidade Orcamentaria')['Especificacao'].to_dict()
    df_executado['Unidade Orcamentaria Mapeada'] = df_executado['Unidade Orcamentaria'].replace(mapeamento_dict)

    # 2. Agrupar os gastos executados por órgão, incluindo Empenhado e Liquidado
    gastos_executados_por_orgao = df_executado.groupby('Unidade Orcamentaria Mapeada')[['Empenhado', 'Liquidado']].sum().reset_index()

    # 3. Juntar com os dados do LOA para ter o valor orçado, o código e o órgão.
    df_comparacao = pd.merge(
        gastos_executados_por_orgao,
        df_loa_orgaos[['Especificacao', 'Valor', 'Codigo']].rename(columns={'Especificacao': 'Unidade Orcamentaria Mapeada', 'Valor': 'Valor Orçado'}),
        on='Unidade Orcamentaria Mapeada',
        how='left'
    )
    df_comparacao = df_comparacao.rename(columns={'Unidade Orcamentaria Mapeada': 'Órgão'})
    df_comparacao = df_comparacao[df_comparacao['Órgão'] != 'TOTAL']
    df_comparacao = df_comparacao.dropna(subset=['Órgão'])
    df_comparacao.rename(columns={'Codigo': 'Código LOA'}, inplace=True)

    # Calcular a coluna 'Estouro %'
    df_comparacao['Estouro %'] = np.where(
        df_comparacao['Empenhado'] > df_comparacao['Valor Orçado'],
        ((df_comparacao['Empenhado'] - df_comparacao['Valor Orçado']) / df_comparacao['Valor Orçado']) * 100,
        0
    )
    df_comparacao = df_comparacao[['Código LOA', 'Órgão', 'Valor Orçado', 'Empenhado', 'Liquidado', 'Estouro %']]

    # --- Visualização: Gráfico de Barras ---
    st.subheader("Gráfico: Orçamento vs. Gasto por Órgão")
    st.info("O gráfico abaixo mostra a comparação entre o valor orçado e os valores empenhado e liquidado por cada órgão.")
    df_long = pd.melt(df_comparacao, id_vars=['Órgão', 'Código LOA'], value_vars=['Empenhado', 'Liquidado', 'Valor Orçado'],
                      var_name='Tipo de Gasto', value_name='Valor')
    fig_bar = px.bar(df_long, x='Valor', y='Órgão', color='Tipo de Gasto', barmode='group', orientation='h',
                     title='Comparação de Gasto Executado e Orçamento Planejado',
                     labels={'Órgão': 'Órgão / Unidade Orçamentária', 'Valor': 'Valor (R$)'},
                     color_discrete_map={
                         'Valor Orçado': 'rgb(120, 120, 120)', 'Empenhado': 'rgb(34, 139, 34)', 'Liquidado': 'rgb(0, 191, 255)'
                     })
    fig_bar.update_layout(height=800, yaxis_categoryorder='total ascending')
    fig_bar.update_traces(marker_line_width=1, marker_line_color="white")
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Visualização: Tabela e Detalhamento ---
    st.subheader("Tabela de Detalhes do Orçamento")
    st.info("A tabela abaixo apresenta a comparação dos valores e o percentual de **estouro** no orçado com o já executado.")
    df_styled = df_comparacao.copy()
    styled_table = df_styled.style.applymap(color_estouro_percent, subset=pd.IndexSlice[:, ['Estouro %']])
    styled_table = styled_table.format({
        'Valor Orçado': 'R$ {:,.2f}', 'Empenhado': 'R$ {:,.2f}', 'Liquidado': 'R$ {:,.2f}', 'Estouro %': '{:.2f}%'
    })
    st.dataframe(styled_table, use_container_width=True, hide_index=True)
    st.divider()

    st.subheader("Detalhamento das despesas por Órgão Orçamentário")
    st.info("A tabela abaixo apresenta um detalhamento das despesas de acordo com o Órgão selecionado, para uma visão mais detalhada de quais despesas estão relacionadas.")
    orgaos_unicos = df_comparacao['Órgão'].unique()
    orgao_selecionado = st.selectbox("Selecione um órgão para ver as despesas detalhadas:", orgaos_unicos)
    if orgao_selecionado:
        st.subheader(f"Despesas Detalhadas para: {orgao_selecionado}")
        df_detalhes = df_executado[df_executado['Unidade Orcamentaria Mapeada'] == orgao_selecionado]
        st.dataframe(df_detalhes, use_container_width=True)

else:
    st.error("Não foi possível carregar os dados. Verifique os arquivos e tente novamente.")