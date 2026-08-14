from pathlib import Path

from src.portfolio_core import generate_demo_data, load_config


ROOT = Path(__file__).resolve().parents[1]


def test_all_twenty_projects_have_required_deliverables():
    projects = sorted((ROOT / "projetos").iterdir())
    assert len(projects) == 20
    required = {"README.md", "config.json", "pipeline.py", "model.py", "dashboard.py", "analysis.sql"}
    for project in projects:
        assert required.issubset({path.name for path in project.iterdir()})


def test_demo_data_contract():
    config = load_config(ROOT / "projetos" / "01_ecommerce_360")
    df = generate_demo_data(config, rows=100)
    assert len(df) == 100
    assert {"revenue", "profit", "target_class", "target_value"}.issubset(df.columns)
    assert df.record_id.is_unique


def test_all_python_deliverables_compile():
    for project in sorted((ROOT / "projetos").iterdir()):
        for filename in ("pipeline.py", "model.py", "dashboard.py"):
            source = (project / filename).read_text(encoding="utf-8")
            compile(source, str(project / filename), "exec")
