from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for project in sorted((ROOT / "projetos").iterdir()):
        if not project.is_dir():
            continue
        config = json.loads((project / "config.json").read_text(encoding="utf-8"))
        quality = json.loads((project / "data" / "processed" / "quality_report.json").read_text(encoding="utf-8"))
        metrics = json.loads((project / "artifacts" / "metrics.json").read_text(encoding="utf-8"))
        content = f"""# {config['title']}

## Problema de negócio

{config['business_question']}

## Base real utilizada

**{quality['source']}**

- Modo: `{quality['data_mode']}`
- Registros processados: {quality['rows']:,}
- Valores ausentes após tratamento: {quality['missing_values']}
- IDs duplicados identificados: {quality['duplicate_ids']}

Os arquivos brutos não são versionados. Consulte `../../FONTES.md` e execute o script de aquisição antes do pipeline.

## Implementação individual

- `pipeline.py`: converte o esquema original para a camada analítica deste caso.
- `analysis.sql`: calcula tendências, ranking, crescimento e margem sobre a fonte processada.
- `model.py`: treina o modelo `{config['model_type']}` definido para a decisão.
- `dashboard.py`: apresenta indicadores, evolução temporal e recortes executivos.

## Métricas da última execução

```json
{json.dumps(metrics, ensure_ascii=False, indent=2)}
```

## Recomendação executiva

{config['recommendation']}

## Execução

```powershell
python pipeline.py
python model.py
streamlit run dashboard.py
```

## Limitações

Os resultados são analíticos e não devem ser convertidos automaticamente em decisões sobre pessoas. Valide estabilidade temporal, representatividade, viés e custo de erro antes de qualquer uso operacional.
"""
        (project / "README.md").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()

