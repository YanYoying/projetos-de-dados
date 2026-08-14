# Churn de clientes

## Problema de negócio

Quais clientes têm maior risco de abandonar a empresa?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Kaggle E-commerce Churn. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Acionar retenção apenas quando valor esperado superar o custo do incentivo.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
