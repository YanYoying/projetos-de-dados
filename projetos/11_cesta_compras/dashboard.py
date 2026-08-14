from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[2]
path.insert(0, str(ROOT))
from src.portfolio_core import render_dashboard

render_dashboard(Path(__file__).resolve().parent)
