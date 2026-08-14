# Inadimplência

## Problema de negócio

Como o risco da carteira evolui ao longo do tempo?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Banco Central do Brasil. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Ajustar provisões e políticas quando tendência e cenário macro indicarem deterioração.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
