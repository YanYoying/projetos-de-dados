# Anomalias financeiras

## Problema de negócio

Quais transações apresentam comportamento suspeito?

## Base real utilizada

**UCI Default of Credit Card Clients, DOI 10.24432/C55S3H**

- Modo: `real`
- Registros processados: 25,000
- Valores ausentes após tratamento: 0
- IDs duplicados identificados: 0

Os arquivos brutos não são versionados. Consulte `../../FONTES.md` e execute o script de aquisição antes do pipeline.

## Implementação individual

- `pipeline.py`: converte o esquema original para a camada analítica deste caso.
- `analysis.sql`: calcula tendências, ranking, crescimento e margem sobre a fonte processada.
- `model.py`: treina o modelo `classification` definido para a decisão.
- `dashboard.py`: apresenta indicadores, evolução temporal e recortes executivos.

## Métricas da última execução

```json
{
  "accuracy": 0.7528,
  "roc_auc": 0.6998
}
```

## Recomendação executiva

Revisar alertas por risco e valor, calibrando o custo de falsos positivos.

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
