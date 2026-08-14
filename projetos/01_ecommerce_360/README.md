# E-commerce 360°

## Problema de negócio

Quais produtos, vendedores e regiões sustentam receita, margem e satisfação?

## Base real utilizada

**Olist Brazilian E-Commerce (Kaggle, dados comerciais anonimizados)**

- Modo: `real`
- Registros processados: 25,000
- Valores ausentes após tratamento: 17125
- IDs duplicados identificados: 0

Os arquivos brutos não são versionados. Consulte `../../FONTES.md` e execute o script de aquisição antes do pipeline.

## Implementação individual

- `pipeline.py`: converte o esquema original para a camada analítica deste caso.
- `analysis.sql`: calcula tendências, ranking, crescimento e margem sobre a fonte processada.
- `model.py`: treina o modelo `regression` definido para a decisão.
- `dashboard.py`: apresenta indicadores, evolução temporal e recortes executivos.

## Métricas da última execução

```json
{
  "mae": 103.2
}
```

## Recomendação executiva

Concentrar investimento nas combinações de categoria e região com margem positiva e alta satisfação.

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
