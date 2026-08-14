# Segmentação RFM

## Problema de negócio

Quais clientes são valiosos, promissores ou estão em risco?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Aplicar campanhas distintas para clientes VIP, promissores e em risco.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
