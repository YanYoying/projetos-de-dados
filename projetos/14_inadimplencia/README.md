# Inadimplência

## Problema de negócio

Como o risco da carteira evolui ao longo do tempo?

## Base real utilizada

**Banco Central do Brasil, SGS série 21082**

- Modo: `real`
- Registros processados: 184
- Valores ausentes após tratamento: 0
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
  "mae": 0.07
}
```

## Recomendação executiva

Ajustar provisões e políticas quando tendência e cenário macro indicarem deterioração.

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
