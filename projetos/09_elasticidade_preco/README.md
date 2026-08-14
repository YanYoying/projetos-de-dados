# Elasticidade de preço

## Problema de negócio

Como preço e promoção alteram demanda e margem?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Kaggle FMCG. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Testar faixas de preço que maximizem margem, não apenas volume.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
