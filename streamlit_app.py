# dashboard.py (versão de análise anual corrigida)

import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# --- Configuração da Página ---
st.set_page_config(page_title="Monitor Cidadão - Peruíbe 2024", layout="wide", page_icon="🇧🇷")

# --- Título do Dashboard ---
st.title("📊 Monitor Cidadão - Análise de Despesas de Peruíbe (2024)")

# --- Carregamento dos Dados ---
@st.cache_data
def carregar_dados(ano):
    caminho_dados_limpos = f'dados_limpos/despesas_limpo_{ano}.csv'
    try:
        df = pd.read_csv(caminho_dados_limpos, delimiter=';', decimal=',')
        cols_monetarias = ['Empenhado', 'Anulado', 'Liquidado', 'Pago', 'Saldo']
        for col in cols_monetarias:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df['Data Emissao'] = pd.to_datetime(df['Data Emissao'], errors='coerce')
        return df
    except FileNotFoundError:
        return None

df = carregar_dados("2024")

# --- Exibição do Dashboard ---
if df is not None:
    # --- Métricas Principais ---
    st.header("Visão Geral do Ano de 2024")
    total_liquidado = df['Liquidado'].sum()
    total_pago = df['Pago'].sum()
    total_empenhos = len(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Liquidado", f"R$ {total_liquidado:,.2f}")
    col2.metric("Total Pago", f"R$ {total_pago:,.2f}")
    col3.metric("Nº de Empenhos", f"{total_empenhos}")
    
    st.divider()

    # --- Análise de Fornecedores Externos ---
    st.header("🏢 Top 10 Fornecedores Externos")
    st.markdown("Exclui pagamentos para a própria prefeitura, institutos de previdência e impostos.")

    entidades_a_excluir = [
        'PREFEITURA', 'INSTITUTO MUNICIPAL DE PREVIDENCIA', 
        'CAIXA ECONOMICA FEDERAL', 'INSTITUTO NACIONAL DO SEGURO SOCIAL'
    ]
    df_externos = df[~df['Fornecedor'].str.contains('|'.join(entidades_a_excluir), case=False, na=False)]
    top_10_externos = df_externos.groupby('Fornecedor')['Liquidado'].sum().sort_values(ascending=False).head(10)
    
    st.bar_chart(top_10_externos)
    st.dataframe(top_10_externos.map('R$ {:,.2f}'.format).rename("Valor Liquidado (R$)"))

    st.divider()
    
    # --- Análises por Categoria ---
    st.header("🔬 Análise por Categoria")
    col_unidade, col_funcao = st.columns(2)

    with col_unidade:
        st.subheader("Gastos por Unidade Orçamentária")
        gasto_unidade = df.groupby('Unidade Orcamentaria')['Liquidado'].sum().sort_values(ascending=False).head(15)
        st.bar_chart(gasto_unidade)
        st.dataframe(gasto_unidade.map('R$ {:,.2f}'.format).rename("Valor Liquidado (R$)"))

    with col_funcao:
        st.subheader("Gastos por Função do Governo")
        gasto_funcao = df.groupby('Funcao')['Liquidado'].sum().sort_values(ascending=False).head(15)
        st.bar_chart(gasto_funcao)
        st.dataframe(gasto_funcao.map('R$ {:,.2f}'.format).rename("Valor Liquidado (R$)"))
    
    st.divider()

    # --- Análise de Programas ---
    st.header("📋 Top 15 Programas com Maiores Gastos")
    gasto_programa = df.groupby('Programa')['Liquidado'].sum().sort_values(ascending=False).head(15)
    st.bar_chart(gasto_programa)
    st.dataframe(gasto_programa.map('R$ {:,.2f}'.format).rename("Valor Liquidado (R$)"))

    st.divider()
    
    # --- Explorador de Dados ---
    st.header("🔍 Explore todos os dados de 2024")
    st.markdown("Use os filtros e a ordenação nas colunas para explorar.")
    st.dataframe(df)

else:
    st.error("Arquivo 'despesas_limpo_2024.csv' não encontrado em 'dados_limpos/'.")
    st.error("Certifique-se de que você executou o 'main.py' configurado para o ano de 2024.")

print("\n--- Análise de Status de Pagamentos (Liquidado vs. Pago) ---")

try:
    # 1. Calcular os totais
    total_liquidado = df['Liquidado'].sum()
    total_pago = df['Pago'].sum()
    total_nao_pago = total_liquidado - total_pago

    # 2. Preparar dados para o gráfico
    sizes = [total_pago, total_nao_pago]
    
    if total_liquidado > 0:
        labels = [f'Pago\nR$ {total_pago:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."),
                  f'Não Pago\n(Restos a Pagar)\nR$ {total_nao_pago:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")]
        colors = ['#4CAF50', '#FF5733'] # Verde para pago, Laranja/Vermelho para não pago
        explode = (0, 0.05)

        # 3. Criar o gráfico de pizza (donut chart)
        fig, ax = plt.subplots(figsize=(12, 8))
        
        wedges, texts, autotexts = ax.pie(sizes,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          colors=colors,
                                          explode=explode,
                                          pctdistance=0.85,
                                          wedgeprops=dict(width=0.4, edgecolor='w'))

        plt.setp(autotexts, size=14, weight="bold", color="white")

        ax.set_title(f'Status de Pagamentos sobre o Total Liquidado\n(Total: R$ {total_liquidado:,.2f})'.replace(",", "X").replace(".", ",").replace("X", "."),
                     fontweight='bold', size=16, pad=20)
        
        ax.legend(wedges, labels,
                  title="Status",
                  loc="center",
                  bbox_to_anchor=(0.5, 0.5),
                  fontsize=12)

        ax.axis('equal')
        
        # Salva a figura em um arquivo
        plt.savefig('status_pagamentos_anual.png')
        print("✅ Gráfico 'status_pagamentos_anual.png' gerado com sucesso!")

    else:
        print("Total liquidado é zero. Gráfico de pagamentos não foi gerado.")

except Exception as e:
    print(f"❌ Ocorreu um erro ao gerar o gráfico de status de pagamentos: {e}")
