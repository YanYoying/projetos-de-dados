# Propensão à compra

## Problema de negócio

Quem tem maior chance de aceitar uma oferta?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

UCI Bank Marketing. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Ordenar contatos por propensão e limitar campanhas de baixo retorno.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
