from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_config(project_dir: Path) -> dict:
    return json.loads((project_dir / "config.json").read_text(encoding="utf-8"))


def generate_demo_data(config: dict, rows: int = 1200) -> pd.DataFrame:
    rng = np.random.default_rng(config["seed"])
    dates = pd.date_range("2024-01-01", periods=730, freq="D")
    df = pd.DataFrame({
        "record_id": np.arange(1, rows + 1),
        "date": rng.choice(dates, rows),
        "region": rng.choice(["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"], rows),
        "category": rng.choice(["A", "B", "C", "D"], rows, p=[.35, .30, .22, .13]),
        "channel": rng.choice(["Orgânico", "Pago", "Parceiro", "Direto"], rows),
        "quantity": rng.integers(1, 12, rows),
        "unit_value": rng.gamma(4, 25, rows).round(2),
        "cost": rng.gamma(3, 18, rows).round(2),
        "engagement": rng.normal(55, 18, rows).clip(0, 100).round(2),
        "delay_days": rng.poisson(3, rows),
        "satisfaction": rng.integers(1, 6, rows),
    })
    df["revenue"] = (df.quantity * df.unit_value).round(2)
    df["profit"] = (df.revenue - df.cost * df.quantity).round(2)
    signal = .025 * df.engagement - .16 * df.delay_days + .3 * (df.satisfaction - 3)
    probability = 1 / (1 + np.exp(-signal + 1.2))
    df["target_class"] = (rng.random(rows) < probability).astype(int)
    df["target_value"] = (df.revenue * (1 + .006 * df.engagement) + rng.normal(0, 35, rows)).clip(0).round(2)
    return df.sort_values("date").reset_index(drop=True)


def run_pipeline(project_dir: Path) -> dict:
    config = load_config(project_dir)
    output = project_dir / "data" / "processed"
    output.mkdir(parents=True, exist_ok=True)
    df = generate_demo_data(config)
    df["margin_pct"] = np.where(df.revenue != 0, 100 * df.profit / df.revenue, 0).round(2)
    df["month"] = pd.to_datetime(df.date).dt.to_period("M").astype(str)
    df.to_csv(output / "analytics.csv", index=False)
    quality = {
        "rows": len(df), "columns": len(df.columns),
        "duplicate_ids": int(df.record_id.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "revenue": float(df.revenue.sum()), "profit": float(df.profit.sum()),
    }
    (output / "quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    return quality


def train_model(project_dir: Path) -> dict:
    config = load_config(project_dir)
    data_path = project_dir / "data" / "processed" / "analytics.csv"
    if not data_path.exists():
        run_pipeline(project_dir)
    df = pd.read_csv(data_path)
    features = ["region", "category", "channel", "quantity", "unit_value", "cost", "engagement", "delay_days", "satisfaction"]
    categorical = ["region", "category", "channel"]
    numeric = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", StandardScaler(), numeric),
    ])
    classification = config["model_type"] == "classification"
    target = "target_class" if classification else "target_value"
    estimator = RandomForestClassifier(n_estimators=80, random_state=config["seed"], class_weight="balanced") if classification else RandomForestRegressor(n_estimators=80, random_state=config["seed"], n_jobs=-1)
    model = Pipeline([("preprocess", preprocessor), ("model", estimator)])
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=.25, random_state=config["seed"], stratify=df[target] if classification else None)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    if classification:
        probability = model.predict_proba(X_test)[:, 1]
        metrics = {"accuracy": round(float(accuracy_score(y_test, prediction)), 4), "roc_auc": round(float(roc_auc_score(y_test, probability)), 4)}
    else:
        metrics = {"mae": round(float(mean_absolute_error(y_test, prediction)), 2)}
    artifacts = project_dir / "artifacts"
    artifacts.mkdir(exist_ok=True)
    joblib.dump(model, artifacts / "model.joblib")
    (artifacts / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def render_dashboard(project_dir: Path) -> None:
    import plotly.express as px
    import streamlit as st

    config = load_config(project_dir)
    path = project_dir / "data" / "processed" / "analytics.csv"
    if not path.exists():
        run_pipeline(project_dir)
    df = pd.read_csv(path, parse_dates=["date"])
    st.set_page_config(page_title=config["title"], layout="wide")
    st.title(config["title"])
    st.caption(config["business_question"])
    region = st.sidebar.multiselect("Região", sorted(df.region.unique()), default=sorted(df.region.unique()))
    view = df[df.region.isin(region)]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita", f"R$ {view.revenue.sum():,.0f}")
    c2.metric("Lucro", f"R$ {view.profit.sum():,.0f}")
    c3.metric("Margem", f"{100 * view.profit.sum() / max(view.revenue.sum(), 1):.1f}%")
    c4.metric(config["target_label"], f"{100 * view.target_class.mean():.1f}%")
    monthly = view.set_index("date").resample("ME")[["revenue", "profit"]].sum().reset_index()
    left, right = st.columns(2)
    left.plotly_chart(px.line(monthly, x="date", y=["revenue", "profit"], title="Evolução mensal"), width="stretch")
    regional = view.groupby("region", as_index=False)[["revenue", "profit"]].sum()
    right.plotly_chart(px.bar(regional, x="region", y="profit", color="revenue", title="Resultado por região"), width="stretch")
    st.subheader("Recomendação executiva")
    st.info(config["recommendation"])
