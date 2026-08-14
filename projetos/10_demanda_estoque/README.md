# Demanda e estoque

## Problema de negócio

Quais itens correm risco de ruptura ou excesso?

## Base real utilizada

**UCI Online Retail, transações reais de varejo britânico**

- Modo: `real`
- Registros processados: 25,000
- Valores ausentes após tratamento: 0
- IDs duplicados identificados: 27

Os arquivos brutos não são versionados. Consulte `../../FONTES.md` e execute o script de aquisição antes do pipeline.

## Implementação individual

- `pipeline.py`: converte o esquema original para a camada analítica deste caso.
- `analysis.sql`: calcula tendências, ranking, crescimento e margem sobre a fonte processada.
- `model.py`: treina o modelo `regression` definido para a decisão.
- `dashboard.py`: apresenta indicadores, evolução temporal e recortes executivos.

## Métricas da última execução

```json
{
  "mae": 7.15
}
```

## Recomendação executiva

Definir estoque de segurança por volatilidade e tempo de reposição.

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
