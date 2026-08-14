# Desempenho logístico

## Problema de negócio

Onde estão os atrasos e como eles afetam satisfação e recompra?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Priorizar rotas com alto volume, atraso acima do SLA e queda de satisfação.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
