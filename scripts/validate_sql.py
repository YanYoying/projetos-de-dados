from __future__ import annotations

import json
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    results = []
    for project in sorted((ROOT / "projetos").iterdir()):
        if not project.is_dir():
            continue
        sql = (project / "analysis.sql").read_text(encoding="utf-8")
        connection = duckdb.connect()
        try:
            result = connection.execute(sql.replace("data/processed/analytics.csv", str(project / "data" / "processed" / "analytics.csv").replace("\\", "/"))).fetchdf()
            if result.empty:
                raise RuntimeError("consulta não retornou resultados")
            results.append({"project": project.name, "rows": len(result), "columns": list(result.columns)})
            print(f"[SQL OK] {project.name}: {len(result)} linhas")
        finally:
            connection.close()
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    (output / "sql_validation.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(results)} análises SQL validadas.")


if __name__ == "__main__":
    main()

