# 🎯 Transparência Mais - Peruíbe

Este projeto é um portal interativo de dados para democratizar o acesso à informação sobre as despesas públicas da Prefeitura da Estância Balneária de Peruíbe.

Desenvolvido para ser uma ferramenta simples e visual, ele compara o orçamento planejado (Lei Orçamentária Anual - LOA) com o valor que é de fato gasto por cada órgão municipal, permitindo que qualquer cidadão acompanhe e fiscalize a execução do orçamento de forma clara e objetiva.

## 📊 Como Funciona

O painel foi construído usando a biblioteca **Streamlit** e se baseia em uma pipeline de dados automatizada:

1.  **Coleta de Dados**: Um script em Python, utilizando a biblioteca **Playwright**, navega no [Portal da Transparência de Peruíbe](https://transparencia.peruibe2.sp.gov.br/) e faz o download de dados de despesas.
2.  **Limpeza e Tratamento**: Os dados brutos são limpos e estruturados, removendo inconsistências e preparando-os para análise.
3.  **Mapeamento e Análise**: As despesas são comparadas com os dados da LOA, permitindo a criação de gráficos e tabelas que visualizam a relação entre o orçamento e a execução.
4.  **Visualização**: O dashboard é exibido em um painel interativo, com gráficos e tabelas que detalham o gasto de cada órgão.

## 💡 Por que este projeto é importante?

A transparência pública é a base de uma democracia forte. Ao simplificar e apresentar os dados de forma acessível, este projeto capacita o cidadão comum a:

* **Fiscalizar**: Verificar se o dinheiro público está sendo utilizado de acordo com o planejado.
* **Participar**: Acompanhar as decisões e os gastos do governo municipal.
* **Promover a Responsabilidade**: Cobrar por uma gestão eficiente e responsável.

## 🚀 Convite à Participação

Este projeto é uma ferramenta para todos os cidadãos de Peruíbe. Acreditamos que a fiscalização é um ato de cidadania.

**Utilize, compartilhe e ajude a fiscalizar!** Se encontrar alguma inconsistência, erro, ou tiver sugestões para melhorar a plataforma, por favor, abra uma `issue` ou entre em contato. A sua participação é fundamental para o sucesso e aprimoramento contínuo deste trabalho.
