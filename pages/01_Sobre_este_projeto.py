import streamlit as st

st.set_page_config(page_title="Sobre este projeto", layout="wide", page_icon="💡")

st.title("💡 Sobre este Portal")
st.markdown("""
Este painel interativo foi criado para democratizar o acesso à informação sobre as despesas públicas da Prefeitura da Estância Balneária de Peruíbe.

Desenvolvido para ser uma ferramenta simples e visual, ele compara o orçamento planejado (Lei Orçamentária Anual - LOA) com o valor que é de fato gasto por cada órgão municipal, permitindo que qualquer cidadão acompanhe e fiscalize a execução do orçamento de forma clara e objetiva.

### 📊 Como Funciona
O portal foi construído usando a biblioteca **Streamlit** e se baseia em uma pipeline de dados automatizada. Os dados são extraídos diretamente do [Portal da Transparência de Peruíbe](https://transparencia.peruibe2.sp.gov.br/) e processados por um script que limpa e organiza as informações para esta visualização.

### 💡 Por que este projeto é importante?
Acreditamos que a transparência pública é a base de uma democracia forte. Ao simplificar e apresentar os dados de forma acessível, este projeto capacita o cidadão a:
* **Fiscalizar**: Verificar se o dinheiro público está sendo utilizado de acordo com o planejado.
* **Participar**: Acompanhar as decisões e os gastos do governo municipal.
* **Promover a Responsabilidade**: Cobrar por uma gestão eficiente e responsável.

---
### 🤝 Convite à Participação
Este projeto é uma ferramenta para todos os cidadãos de Peruíbe. Acreditamos que a fiscalização é um ato de cidadania.

**Utilize, compartilhe e ajude a fiscalizar!** Se encontrar alguma inconsistência, erro, ou tiver sugestões para melhorar a plataforma, por favor, entre em contato. A sua participação é fundamental para o sucesso e aprimoramento contínuo deste trabalho.
""")