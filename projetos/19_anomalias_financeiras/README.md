# Anomalias financeiras

## Problema de negócio

Quais transações apresentam comportamento suspeito?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

UCI/Kaggle. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Revisar alertas por risco e valor, calibrando o custo de falsos positivos.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
