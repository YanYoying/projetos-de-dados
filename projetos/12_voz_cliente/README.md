# Voz do cliente

## Problema de negócio

Quais causas estão associadas às avaliações negativas?

## Entregáveis

- `dashboard.py`: visão executiva e filtros interativos.
- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.
- `model.py`: modelo preditivo e métricas reproduzíveis.
- `pipeline.py`: ETL com validação e camada analítica.

## Fonte recomendada

Olist Reviews. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.

## Recomendação executiva

Atacar os temas recorrentes com maior impacto em satisfação e receita.

## Como executar

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```
