# Cesta de compras

## Problema de negócio

Quais produtos apresentam maior afinidade de compra?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Criar combos somente quando lift e margem incremental forem positivos.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
