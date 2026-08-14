# Pipeline empresarial

## Problema de negócio

Como entregar indicadores confiáveis e atualizados?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist SQLite. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Monitorar qualidade, linhagem e atualização antes de publicar indicadores.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
