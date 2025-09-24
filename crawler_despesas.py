# main.py (versão com correções aplicadas)

import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# --- CONFIGURAÇÃO ---
ANO = "2024"
DATA_INICIO = f"01/01/{ANO}"
DATA_FIM = f"31/12/{ANO}"

# --- FUNÇÃO DE COLETA DE DADOS ---
def baixar_dados_filtrados(ano, data_inicio, data_fim):
    filter_url = 'https://transparencia.peruibe2.sp.gov.br/filtros-despesasorcamentarias'
    OPERACAO_TIMEOUT = 300 * 1000 # 5 minutos

    with sync_playwright() as p:
        print("🚀 Iniciando o navegador em modo VISÍVEL...")
        browser = p.chromium.launch(headless=False) # MANTENDO O MODO VISÍVEL
        
        page = browser.new_page()
        page.set_default_timeout(OPERACAO_TIMEOUT)

        try:
            print(f"➡️  Etapa 1: Navegando para a página de filtros...")
            page.goto(filter_url)
            print("✅ Página de filtros carregada.")

            print(f"\n➡️  Etapa 2: Selecionando o ano de {ano}...")
            page.select_option('#vEXERCICIO_MPAGE', ano)
            print(f"✅ Ano {ano} selecionado.")
            
            print(f"\n➡️  Etapa 3: Preenchendo o formulário com as datas (em modo lento)...")
            
            # ##################################################################
            # MUDANÇA APLICADA AQUI: Usando page.type() com delay
            # ##################################################################
            page.type('#W0012vDATAINICIAL', data_inicio, delay=150)
            page.type('#W0012vDATAFINAL', data_fim, delay=150)
            
            print(f"✅ Datas preenchidas: {data_inicio} a {data_fim}.")
            
            print("\n➡️  Etapa 4: Aplicando o filtro (pode levar vários minutos)...")
            page.click('#W0012BTNENTER')
            
            print(f"...Aguardando o servidor processar os dados de {ano}...")
            page.wait_for_url("**/resultado-despesaorcamentaria-posicao-atual")
            page.wait_for_load_state('networkidle')
            print("✅ Página de resultados carregada com os dados filtrados.")

            print("\n➡️  Etapa 5: Exportando o arquivo CSV...")
            with page.expect_download() as download_info:
                print("...Clicando no botão de dropdown de exportação...")
                button_selector = '#DDO_ACTIONGROUPEXPORTContainer_btnGroupDrop'
                page.wait_for_selector(button_selector, state='visible')
                page.click(button_selector)
                
                page.wait_for_timeout(500)
                
                print("...Clicando na opção CSV...")
                csv_option_selector = 'a:has(img[src="/Resources/ActionCSV.png"])'
                page.locator(csv_option_selector).click()
            
            download = download_info.value
            
            os.makedirs("downloads", exist_ok=True)
            caminho_arquivo = os.path.join("downloads", f"despesas_bruto_{ano}.csv")
            
            download.save_as(caminho_arquivo)
            print(f"✅ Download concluído! Arquivo bruto de {ano} salvo em: '{caminho_arquivo}'")
            return caminho_arquivo

        finally:
            print("\n🔒 Fechando o navegador...")
            browser.close()

# --- FUNÇÃO DE LIMPEZA DE DADOS CORRIGIDA ---
def limpar_dados(caminho_arquivo_bruto, ano):
    print(f"\n➡️  Etapa 6: Limpando o arquivo {caminho_arquivo_bruto}...")
    
    df = pd.read_csv(
        caminho_arquivo_bruto, 
        delimiter=';', 
        encoding='utf-8', 
        thousands=',',
        dtype={'Data Emissão': str},
        decimal='.'
    )

    num_registos_bruto = df.shape[0]
    print(f"Número de registos no carregamento: {num_registos_bruto}")
    
    df.columns = [
        'Empenho', 'Data Emissão', 'CPF/CNPJ', 'Fornecedor', 
        'Unidade Orcamentaria', 'Unidade Executora', 'Programa', 
        'Modalidade', 'Fundamento Legal', 'Processo', 'Funcao', 
        'Subfuncao', 'Objeto Contratacao', 'Empenhado', 'Anulado', 
        'Liquidado', 'Pago', 'Saldo'
    ]
    
    # 🚨 PONTO CORRIGIDO: Limpa a string da data antes de convertê-la
    df['Data Emissão'] = df['Data Emissão'].astype(str).str.strip()  # Remove espaços em branco
    df['Data Emissão'] = df['Data Emissão'].str.zfill(8)
    df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], format='%d%m%Y', errors='coerce')
    
    # Remove as linhas onde a data não pôde ser convertida (estavam com NaT)
    df.dropna(subset=['Data Emissão'], inplace=True)
    num_registos_limpo = df.shape[0]
    
    print(f"Número de registos válidos depois da limpeza: {num_registos_limpo}")
    print(f"Foram removidos {num_registos_bruto - num_registos_limpo} registos com datas inválidas ou formatadas incorretamente.")

    df['Objeto Contratacao'] = df['Objeto Contratacao'].fillna('Não especificado')
    print("✅ Limpeza concluída.")
    
    os.makedirs("dados_limpos", exist_ok=True)
    caminho_arquivo_limpo = os.path.join("dados_limpos", f"despesas_limpo_{ano}.csv")
    
    # Salvando o arquivo limpo
    df.to_csv(caminho_arquivo_limpo, sep=';', index=False, encoding='utf-8-sig', decimal=',')
    print(f"✅ Arquivo limpo salvo em: '{caminho_arquivo_limpo}'")
    
    return caminho_arquivo_limpo
    print(f"\n➡️  Etapa 6: Limpando o arquivo {caminho_arquivo_bruto}...")
    
    # 🚨 CORREÇÃO PRINCIPAL AQUI:
    # 1. 'dtype' para ler a 'Data Emissão' como string e preservar zeros à esquerda.
    # 2. 'decimal' para que o pandas interprete a vírgula (',') como separador decimal.
    df = pd.read_csv(
        caminho_arquivo_bruto, 
        delimiter=';', 
        encoding='utf-8', 
        thousands=',',
        dtype={'Data Emissão': str},
        decimal='.'
    )

    # Obtém o número de linhas (registos)
    num_registos = df.shape[0]
    print(f"Número de registos no carregamento: {num_registos}")
    
    df.columns = [
        'Empenho', 'Data Emissão', 'CPF/CNPJ', 'Fornecedor', 
        'Unidade Orcamentaria', 'Unidade Executora', 'Programa', 
        'Modalidade', 'Fundamento Legal', 'Processo', 'Funcao', 
        'Subfuncao', 'Objeto Contratacao', 'Empenhado', 'Anulado', 
        'Liquidado', 'Pago', 'Saldo'
    ]
    
    # ❌ ESTE BLOCO FOI REMOVIDO
    # df['Data Emissão'] = df['Data Emissão'].astype(str).str.zfill(8)
    # df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], format='%d%m%Y', errors='coerce')
    
    # ✅ ESTE BLOCO ESTÁ NOVO E SUBSTITUI A PARTE ACIMA:
    # Garante que a data tem 8 dígitos e converte para o formato datetime
    df['Data Emissão'] = df['Data Emissão'].astype(str).str.zfill(8)
    df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], format='%d%m%Y', errors='coerce')

    df['Objeto Contratacao'] = df['Objeto Contratacao'].fillna('Não especificado')
    print("✅ Limpeza concluída.")
    
    os.makedirs("dados_limpos", exist_ok=True)
    caminho_arquivo_limpo = os.path.join("dados_limpos", f"despesas_limpo_{ano}.csv")
    
    num_registos = df.shape[0]
    print(f"Número de registos depois da limpeza: {num_registos}")

    # ⚠️ ATENÇÃO: Ao salvar o arquivo, o pandas precisa saber que o separador decimal é a vírgula
    df.to_csv(caminho_arquivo_limpo, sep=';', index=False, encoding='utf-8-sig', decimal=',')
    print(f"✅ Arquivo limpo salvo em: '{caminho_arquivo_limpo}'")
    
    return caminho_arquivo_limpo

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    try:
        #aminho_bruto = baixar_dados_filtrados(ANO, DATA_INICIO, DATA_FIM)
        caminho_bruto = os.path.join("downloads", f"despesas_bruto_2024_full.csv")
        #caminho_limpo = limpar_dados(caminho_bruto, ANO)
        caminho_limpo = limpar_dados(caminho_bruto, ANO)
        print(f"\n🎉🎉🎉 PROCESSO CONCLUÍDO COM SUCESSO! 🎉🎉🎉")
        print(f"Seus dados limpos para o ano de {ANO} estão prontos em: {caminho_limpo}")
    except Exception as e:
        print(f"\n❌ OCORREU UM ERRO GERAL NO PROCESSO: {e}")