import streamlit as st

st.set_page_config(page_title="Como ler estas informações", layout="wide", page_icon="📚")

st.title("📚 Como ler estas informações")
st.markdown("""
### Entendendo os Dados do Orçamento

Aqui estão algumas definições simples para ajudar na sua análise:

* **Orçado**: É o valor que o município planejou gastar com cada órgão ao longo do ano. É o "teto" de gastos aprovado na Lei Orçamentária Anual (LOA).
* **Empenhado**: É a primeira fase do gasto. O valor empenhado é um compromisso da Prefeitura de que o dinheiro será usado para um propósito específico (por exemplo, a compra de um material de escritório ou a contratação de um serviço).
* **Liquidado**: É a segunda fase do gasto. Significa que o serviço já foi prestado ou o material foi entregue, e o valor devido foi confirmado. O município reconhece que a dívida existe.
* **Pago**: É a fase final. Significa que a dívida foi quitada e o dinheiro, de fato, saiu dos cofres públicos.

A tabela na página principal compara o valor planejado com o gasto real de cada órgão. Preste atenção na coluna **"Estouro %"**. Ela mostra o quanto o valor empenhado está acima do orçado. Para facilitar, usamos um sistema de cores:
* **Verde**: Se não houve estouro (0%).
* **Amarelo**: Se o estouro foi de até 5%.
* **Vermelho**: Se o estouro foi superior a 5%.
""")