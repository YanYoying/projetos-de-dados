# Mobilidade urbana

## Problema de negócio

Onde e quando existe maior demanda por transporte?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

NYC TLC. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Reposicionar oferta para zonas e horários de demanda recorrente.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
