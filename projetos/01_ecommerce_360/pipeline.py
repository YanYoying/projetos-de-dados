from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[2]
path.insert(0, str(ROOT))
from src.portfolio_core import run_pipeline

if __name__ == '__main__':
    print(run_pipeline(Path(__file__).resolve().parent))
