#  ETL e Análise de Manutenção Industrial

Projeto de ETL e análise de dados industriais utilizando Python (Pandas) e Power BI.

O objetivo deste projeto é simular um pipeline completo de dados industriais, desde a geração de dados até o tratamento e análise em dashboards de Business Intelligence.

---

#  Objetivo do Projeto:

- Simular dados industriais de manutenção e produção
- Construir pipeline de ETL em Python
- Tratar e estruturar dados para análise
- Validar integridade entre tabelas
- Criar base analítica para Power BI
- Desenvolver indicadores operacionais (KPIs)
- Aplicar boas práticas de organização de projetos de dados

---

#  Contexto:

O projeto simula um ambiente industrial contendo informações sobre:

- máquinas
- falhas
- manutenções
- produção
- análise FMEA

---

#  Fluxo do Projeto:

geracao de dados → dados brutos → ETL → dados tratados → Power BI

Este projeto segue uma estrutura dimensional(modelo estrela)

                maquinas
               /    |    \
         falhas manutencao producao
                    |
                  fmea

---

# Estrutura do Projeto:
```text id="flow_01"

etl-manutencao-industrial/
│
├── geracao_dados/
│   ├── geracao_fmea.py
│   ├── geracao_coilcoating.py
│
├── dados/
│   ├── falhas.csv
│   ├── maquinas.csv
│   ├── manutencao.csv
│   ├── producao.csv
│   └── fmea.csv
│
├── dados_tratados/
│   ├── falhas_tratada.csv
│   ├── maquinas_tratada.csv
│   ├── manutencao_tratada.csv
│   ├── producao_tratada.csv
│   └── fmea_tratada.csv
│
├── scripts/
│   └── estudoetl.py
│
├── powerbi/
│   └── dashboard.pbix
│
└── README.md
