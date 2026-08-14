# Funil de marketing

## Problema de negócio

Quais canais entregam conversão e retorno sobre investimento?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Kaggle Sales & Marketing. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Realocar verba de canais com CAC alto para canais de maior conversão e LTV.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
