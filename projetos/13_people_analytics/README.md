# People Analytics

## Problema de negócio

Quais fatores estão associados à saída de funcionários?

## Base real utilizada

**UCI Absenteeism at Work, registros reais de uma empresa brasileira**

- Modo: `real`
- Registros processados: 740
- Valores ausentes após tratamento: 0
- IDs duplicados identificados: 704

Os arquivos brutos não são versionados. Consulte `../../FONTES.md` e execute o script de aquisição antes do pipeline.

## Implementação individual

- `pipeline.py`: converte o esquema original para a camada analítica deste caso.
- `analysis.sql`: calcula tendências, ranking, crescimento e margem sobre a fonte processada.
- `model.py`: treina o modelo `classification` definido para a decisão.
- `dashboard.py`: apresenta indicadores, evolução temporal e recortes executivos.

## Métricas da última execução

```json
{
  "accuracy": 0.7459,
  "roc_auc": 0.8445
}
```

## Recomendação executiva

Usar o risco para orientar diagnóstico humano, nunca decisões automáticas de desligamento.

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
