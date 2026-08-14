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
from src.real_sources import load_real_data


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
    df, source = load_real_data(project_dir.name)
    if len(df) > 25_000:
        df = df.sample(25_000, random_state=config["seed"]).sort_values("date").reset_index(drop=True)
    df["margin_pct"] = np.where(df.revenue != 0, 100 * df.profit / df.revenue, 0).round(2)
    df["month"] = pd.to_datetime(df.date).dt.to_period("M").astype(str)
    df.to_csv(output / "analytics.csv", index=False)
    quality = {
        "rows": len(df), "columns": len(df.columns),
        "duplicate_ids": int(df.record_id.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "revenue": float(df.revenue.sum()), "profit": float(df.profit.sum()),
        "source": source, "data_mode": "real",
    }
    (output / "quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    return quality


def train_model(project_dir: Path) -> dict:
    config = load_config(project_dir)
    data_path = project_dir / "data" / "processed" / "analytics.csv"
    if not data_path.exists():
        run_pipeline(project_dir)
    df = pd.read_csv(data_path)
    df["year"] = pd.to_datetime(df["date"], errors="coerce", format="mixed").dt.year.fillna(0)
    df["month_num"] = pd.to_datetime(df["date"], errors="coerce", format="mixed").dt.month.fillna(0)
    default_features = ["region", "category", "channel", "quantity", "unit_value", "cost", "engagement", "delay_days", "satisfaction", "year", "month_num"]
    feature_overrides = {
        "01_ecommerce_360": ["region", "category", "channel", "engagement", "delay_days", "satisfaction", "year", "month_num"],
        "02_desempenho_logistico": ["region", "category", "channel", "quantity", "unit_value", "cost", "engagement", "satisfaction", "year", "month_num"],
        "03_segmentacao_rfm": ["region", "category", "channel", "engagement", "delay_days", "satisfaction", "year", "month_num"],
        "04_previsao_vendas": ["region", "category", "channel", "engagement", "delay_days", "satisfaction", "year", "month_num"],
        "07_propensao_compra": ["region", "category", "channel", "quantity", "cost", "delay_days", "year", "month_num"],
        "08_rentabilidade_comercial": ["region", "category", "channel", "engagement", "delay_days", "satisfaction", "year", "month_num"],
        "09_elasticidade_preco": ["region", "category", "channel", "unit_value", "engagement", "year", "month_num"],
        "10_demanda_estoque": ["region", "category", "channel", "unit_value", "engagement", "year", "month_num"],
        "12_voz_cliente": ["region", "category", "channel", "quantity", "unit_value", "cost", "engagement", "delay_days", "year", "month_num"],
        "14_inadimplencia": ["year", "month_num"],
        "15_mobilidade_urbana": ["region", "category", "channel", "quantity", "unit_value", "cost", "engagement", "year", "month_num"],
        "16_bicicletas_compartilhadas": ["region", "category", "channel", "quantity", "cost", "satisfaction", "year", "month_num"],
        "18_saude_publica": ["year", "month_num"],
    }
    features = feature_overrides.get(project_dir.name, default_features)
    categorical = [column for column in ["region", "category", "channel"] if column in features]
    numeric = [c for c in features if c not in categorical]
    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", StandardScaler(), numeric),
    ])
    classification = config["model_type"] == "classification"
    target = "target_class" if classification else "target_value"
    estimator = RandomForestClassifier(n_estimators=60, random_state=config["seed"], class_weight="balanced", n_jobs=-1) if classification else RandomForestRegressor(n_estimators=60, random_state=config["seed"], n_jobs=-1)
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
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", format="mixed")
    df = df.dropna(subset=["date"])
    st.set_page_config(page_title=config["title"], layout="wide")
    st.title(config["title"])
    st.caption(config["business_question"])
    region = st.sidebar.multiselect("Região", sorted(df.region.unique()), default=sorted(df.region.unique()))
    view = df[df.region.isin(region)]
    slug = project_dir.name
    classification_projects = {"03_segmentacao_rfm", "05_churn_clientes", "06_funil_marketing", "07_propensao_compra", "11_cesta_compras", "12_voz_cliente", "13_people_analytics", "17_analytics_digital", "19_anomalias_financeiras", "20_pipeline_empresarial"}
    operational_projects = {"02_desempenho_logistico", "09_elasticidade_preco", "10_demanda_estoque", "14_inadimplencia", "15_mobilidade_urbana", "16_bicicletas_compartilhadas", "18_saude_publica"}
    metrics_path = project_dir / "artifacts" / "metrics.json"
    model_metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}
    c1, c2, c3, c4 = st.columns(4)
    if slug in classification_projects:
        labels = {
            "05_churn_clientes": ("Clientes", "Churn observado"), "06_funil_marketing": ("Leads", "Conversão"),
            "07_propensao_compra": ("Clientes", "Aceite observado"), "11_cesta_compras": ("Pedidos", "Cestas complexas"),
            "12_voz_cliente": ("Avaliações", "Avaliações negativas"), "13_people_analytics": ("Registros", "Ausência elevada"),
            "17_analytics_digital": ("Leads digitais", "Conversão"), "19_anomalias_financeiras": ("Clientes", "Default observado"),
            "20_pipeline_empresarial": ("Registros", "Não entregues"), "03_segmentacao_rfm": ("Clientes", "Alto valor")}
        count_label, rate_label = labels[slug]
        c1.metric(count_label, f"{len(view):,}")
        c2.metric(rate_label, f"{100 * view.target_class.mean():.1f}%")
        c3.metric("Engajamento médio", f"{view.engagement.mean():.1f}")
        c4.metric("ROC AUC", f"{model_metrics.get('roc_auc', 0):.3f}")
        monthly = view.set_index("date").resample("ME").agg(volume=("record_id", "count"), taxa=("target_class", "mean")).reset_index()
        chart_columns = ["volume", "taxa"]
        regional = view.groupby("region", as_index=False).agg(volume=("record_id", "count"), taxa=("target_class", "mean"))
        regional_y, regional_color = "taxa", "volume"
    elif slug in operational_projects:
        labels = {"02_desempenho_logistico":"Tempo médio de entrega", "09_elasticidade_preco":"Quantidade média", "10_demanda_estoque":"Demanda média", "14_inadimplencia":"Indicador médio", "15_mobilidade_urbana":"Duração média (min)", "16_bicicletas_compartilhadas":"Duração média (min)", "18_saude_publica":"Taxa média"}
        c1.metric("Registros", f"{len(view):,}")
        c2.metric(labels[slug], f"{view.target_value.mean():,.2f}")
        c3.metric("Valor mais recente", f"{view.sort_values('date').target_value.iloc[-1]:,.2f}")
        c4.metric("MAE do modelo", f"{model_metrics.get('mae', 0):,.2f}")
        monthly = view.set_index("date").resample("ME").agg(volume=("record_id", "count"), indicador=("target_value", "mean")).reset_index()
        chart_columns = ["volume", "indicador"]
        regional = view.groupby("region", as_index=False).agg(volume=("record_id", "count"), indicador=("target_value", "mean"))
        regional_y, regional_color = "indicador", "volume"
    else:
        c1.metric("Receita", f"R$ {view.revenue.sum():,.0f}")
        c2.metric("Resultado", f"R$ {view.profit.sum():,.0f}")
        c3.metric("Margem", f"{100 * view.profit.sum() / max(view.revenue.sum(), 1):.1f}%")
        c4.metric("MAE do modelo", f"{model_metrics.get('mae', 0):,.2f}")
        monthly = view.set_index("date").resample("ME")[["revenue", "profit"]].sum().reset_index()
        chart_columns = ["revenue", "profit"]
        regional = view.groupby("region", as_index=False)[["revenue", "profit"]].sum()
        regional_y, regional_color = "profit", "revenue"
    left, right = st.columns(2)
    left.plotly_chart(px.line(monthly, x="date", y=chart_columns, title="Evolução mensal"), width="stretch")
    right.plotly_chart(px.bar(regional, x="region", y=regional_y, color=regional_color, title="Resultado por segmento"), width="stretch")
    st.subheader("Recomendação executiva")
    st.info(config["recommendation"])
