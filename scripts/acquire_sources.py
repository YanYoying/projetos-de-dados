from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data_sources"

URLS = {
    "olist.zip": "https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce",
    "olist_marketing.zip": "https://www.kaggle.com/api/v1/datasets/download/olistbr/marketing-funnel-olist",
    "bank.zip": "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip",
    "iranian_churn.zip": "https://archive.ics.uci.edu/static/public/563/iranian+churn+dataset.zip",
    "online_retail.zip": "https://archive.ics.uci.edu/static/public/352/online+retail.zip",
    "absenteeism.zip": "https://archive.ics.uci.edu/static/public/445/absenteeism+at+work.zip",
    "credit_default.zip": "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip",
    "bcb_inadimplencia.csv": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.21082/dados?formato=csv",
    "nyc_taxi_2025_01.parquet": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet",
    "citibike.zip": "https://s3.amazonaws.com/tripdata/JC-202501-citibike-tripdata.csv.zip",
    "worldbank_mortality.json": "https://api.worldbank.org/v2/country/BRA/indicator/SH.DYN.MORT?format=json&per_page=100",
}


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    manifest = []
    for filename, url in URLS.items():
        target = OUTPUT / filename
        if not target.exists():
            print(f"Baixando {filename}...")
            urllib.request.urlretrieve(url, target)
        manifest.append({"file": filename, "url": url, "bytes": target.stat().st_size})
        print(f"[OK] {filename}: {target.stat().st_size:,} bytes")
    manifest_path = OUTPUT / "manifest.json"
    manifest_path.write_text(json.dumps({"retrieved_at": datetime.now(timezone.utc).isoformat(), "sources": manifest}, indent=2), encoding="utf-8")
    print(f"Manifesto local: {manifest_path}")


if __name__ == "__main__":
    main()

