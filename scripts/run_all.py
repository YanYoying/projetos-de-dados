from __future__ import annotations

import json
from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))
from src.portfolio_core import run_pipeline, train_model


def main() -> None:
    results = []
    for project in sorted((ROOT / "projetos").iterdir()):
        if not project.is_dir():
            continue
        quality = run_pipeline(project)
        metrics = train_model(project)
        results.append({"project": project.name, "status": "ok", "quality": quality, "metrics": metrics})
        print(f"[OK] {project.name}: {metrics}")
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    (output / "execution_summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n{len(results)} projetos executados com sucesso.")


if __name__ == "__main__":
    main()

