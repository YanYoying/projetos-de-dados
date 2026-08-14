# Bicicletas compartilhadas

## Problema de negócio

Quais estações precisam de rebalanceamento?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

BigQuery Citi Bike. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Rebalancear estações antes dos picos previstos, minimizando viagens operacionais.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
