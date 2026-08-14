# People Analytics

## Problema de negócio

Quais fatores estão associados à saída de funcionários?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

IBM HR Attrition. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Usar o risco para orientar diagnóstico humano, nunca decisões automáticas de desligamento.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
