# Modelagem Estatística para Previsão de Gols no Futebol

## 📌 Objetivo do Projeto

O objetivo deste projeto foi utilizar **bases históricas disponibilizadas na própria internet** para construir **modelos estatísticos capazes de prever a ocorrência de gols em partidas de futebol**.

A proposta é explorar dados reais, transformando-os em variáveis relevantes para análise e modelagem preditiva, com foco em eventos relacionados a gols (ex.: over/under, ambas marcam, etc.).

---

## 📊 Metodologia

- Coleta e organização de dados históricos de partidas de futebol
- Utilização de informações fornecidas por casas de apostas (odds e mercados)
- Pré-processamento e limpeza dos dados
- Construção de modelos estatísticos (ex.: regressão logística)
- Avaliação do desempenho preditivo dos modelos

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- Pandas
- NumPy
- Scikit-learn
- Jupyter Notebook / Scripts `.py`
- BeautifulSoup

---

## 📁 Estrutura do Projeto

```text
.
├── base.geral.csv/                 # Bases históricas utilizadas
├── historico.jogos/                # Scripts de coleta e tratamento de dados
├── modelo-logistico-gols0+.py/     # Modelo estatístico para ter pelo menos 1 gol
├── modelo-logistico-gols1+.py/     # Modelo estatístico para mais de 1 gol
└── README.md