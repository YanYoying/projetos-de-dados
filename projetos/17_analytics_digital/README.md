# Analytics digital

## Problema de negócio

Quais canais e páginas contribuem para conversão?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Google Analytics Sample. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Otimizar etapas com maior abandono e avaliar canais por receita incremental.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
