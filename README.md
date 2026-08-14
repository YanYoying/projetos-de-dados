# Projetos de Dados

Portfólio empresarial com 20 projetos completos de análise de dados. Cada projeto contém:

- dashboard executivo em Streamlit;
- análise SQL com CTEs, funções de janela e indicadores;
- modelo preditivo em Python;
- pipeline ETL reproduzível;
- documentação do problema, métricas e recomendações.

## Execução rápida

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/acquire_sources.py
python scripts/run_all.py
python scripts/validate_sql.py
streamlit run projetos/01_ecommerce_360/dashboard.py
```

Os pipelines usam dados sintéticos determinísticos para que todo o repositório funcione imediatamente. Cada README indica a fonte pública recomendada para substituir a demonstração por dados reais.

## Projetos recomendados para recrutamento

Comece por estes cinco estudos. Eles cobrem BI, SQL, Python, machine learning e engenharia de dados sem repetir a mesma história:

| Projeto | Competência principal | Evidência |
|---|---|---|
| [E-commerce 360°](projetos/01_ecommerce_360/) | Dashboard executivo e SQL | R$ 4,06 milhões analisados em 25 mil pedidos |
| [Churn de clientes](projetos/05_churn_clientes/) | Classificação em Python | ROC AUC de 0,956 em dados reais de telecom |
| [Funil de marketing](projetos/06_funil_marketing/) | Marketing analytics | 8 mil leads e conversão observada de 10,5% |
| [Demanda e estoque](projetos/10_demanda_estoque/) | Forecast e varejo | 25 mil transações reais de varejo |
| [Pipeline empresarial](projetos/20_pipeline_empresarial/) | ETL e qualidade | Pipeline reproduzível com relatório de qualidade |

Veja [DESTAQUES.md](DESTAQUES.md) para resultados e narrativa de apresentação e [GUIA_ENTREVISTA.md](GUIA_ENTREVISTA.md) para preparação técnica.

## Catálogo completo

| # | Projeto | Área | Decisão suportada |
|---|---|---|---|
| 01 ⭐ | E-commerce 360° | Varejo | Receita, margem e satisfação |
| 02 | Desempenho logístico | Operações | SLA e atrasos |
| 03 | Segmentação RFM | CRM | Campanhas por segmento |
| 04 | Previsão de vendas | Planejamento | Metas e capacidade |
| 05 ⭐ | Churn de clientes | Retenção | Priorização de clientes em risco |
| 06 ⭐ | Funil de marketing | Marketing | CAC, conversão e ROI |
| 07 | Propensão à compra | Comercial | Priorização de ofertas |
| 08 | Rentabilidade comercial | Finanças | Portfólio, margem e descontos |
| 09 | Elasticidade de preço | Pricing | Preço ótimo |
| 10 ⭐ | Demanda e estoque | Supply chain | Reposição e ruptura |
| 11 | Cesta de compras | Varejo | Combos e cross-sell |
| 12 | Voz do cliente | CX | Causas de insatisfação |
| 13 | People Analytics | RH | Redução de turnover |
| 14 | Inadimplência | Risco | Monitoramento de carteira |
| 15 | Mobilidade urbana | Transporte | Oferta por região e horário |
| 16 | Bicicletas compartilhadas | Operações | Rebalanceamento de estações |
| 17 | Analytics digital | Produto | Conversão e atribuição |
| 18 | Saúde pública | Saúde | Priorização territorial |
| 19 | Anomalias financeiras | Fraude | Alertas de transações |
| 20 ⭐ | Pipeline empresarial | Engenharia | Dados confiáveis e atualizados |

## Estrutura de cada pasta

```text
dashboard.py      painel executivo
analysis.sql      SQL analítico avançado
model.py          treinamento e métricas
pipeline.py       extração, transformação e carga
config.json       definição do caso de negócio
README.md         narrativa para apresentação
data/processed/   saída gerada localmente
artifacts/        modelo e métricas
```

## Validação

`python scripts/run_all.py` executa os pipelines e modelos dos 20 projetos e grava um resumo em `artifacts/execution_summary.json`.

`python scripts/validate_sql.py` executa as vinte análises SQL no DuckDB e confirma que todas produzem resultados.

Consulte [FONTES.md](FONTES.md) para baixar as bases reais e conferir licença, origem e finalidade de cada conjunto.
