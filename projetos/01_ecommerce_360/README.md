# E-commerce 360°

## Problema de negócio

Quais produtos, vendedores e regiões sustentam receita, margem e satisfação?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Concentrar investimento nas combinações de categoria e região com margem positiva e alta satisfação.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
