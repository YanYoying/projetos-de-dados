# Rentabilidade comercial

## Problema de negócio

Quais produtos vendem muito, mas reduzem a margem?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Tableau Superstore. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Rever descontos de itens com grande receita e lucro baixo ou negativo.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
