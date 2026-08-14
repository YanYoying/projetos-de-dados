from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data_sources"


def _read_zip(zip_name: str, member: str, **kwargs) -> pd.DataFrame:
    with zipfile.ZipFile(SOURCES / zip_name) as archive:
        return pd.read_csv(archive.open(member), **kwargs)


def _base_frame(rows: int) -> pd.DataFrame:
    return pd.DataFrame(index=range(rows))


def _finish(df: pd.DataFrame) -> pd.DataFrame:
    defaults = {
        "record_id": np.arange(1, len(df) + 1), "date": pd.Timestamp("2024-01-01"),
        "region": "Não informado", "category": "Não informado", "channel": "Não informado",
        "quantity": 1, "unit_value": 0.0, "cost": 0.0, "engagement": 0.0,
        "delay_days": 0.0, "satisfaction": 3.0, "revenue": 0.0, "profit": 0.0,
        "target_class": 0, "target_value": 0.0,
    }
    for column, value in defaults.items():
        if column not in df:
            df[column] = value
    for column in ("region", "category", "channel"):
        df[column] = df[column].fillna("Não informado").astype(str)
    df["date"] = pd.to_datetime(df.date, errors="coerce").fillna(pd.Timestamp("2024-01-01"))
    for column in ("quantity", "unit_value", "cost", "engagement", "delay_days", "satisfaction", "revenue", "profit", "target_value"):
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)
    df["target_class"] = pd.to_numeric(df.target_class, errors="coerce").fillna(0).astype(int)
    return df.reset_index(drop=True)


def load_olist(slug: str) -> tuple[pd.DataFrame, str]:
    orders = _read_zip("olist.zip", "olist_orders_dataset.csv")
    items = _read_zip("olist.zip", "olist_order_items_dataset.csv")
    payments = _read_zip("olist.zip", "olist_order_payments_dataset.csv")
    customers = _read_zip("olist.zip", "olist_customers_dataset.csv")
    reviews = _read_zip("olist.zip", "olist_order_reviews_dataset.csv")
    products = _read_zip("olist.zip", "olist_products_dataset.csv")
    item_agg = items.groupby("order_id", as_index=False).agg(quantity=("order_item_id", "count"), revenue=("price", "sum"), freight=("freight_value", "sum"), product_id=("product_id", "first"), seller_count=("seller_id", "nunique"))
    pay_agg = payments.groupby("order_id", as_index=False).agg(payment_value=("payment_value", "sum"), installments=("payment_installments", "max"), payment_type=("payment_type", "first"))
    review_agg = reviews.groupby("order_id", as_index=False).agg(satisfaction=("review_score", "mean"), review_text=("review_comment_message", "first"))
    df = orders.merge(item_agg, on="order_id", how="left").merge(pay_agg, on="order_id", how="left").merge(review_agg, on="order_id", how="left").merge(customers, on="customer_id", how="left").merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    delivered = pd.to_datetime(df.order_delivered_customer_date, errors="coerce")
    estimated = pd.to_datetime(df.order_estimated_delivery_date, errors="coerce")
    purchased = pd.to_datetime(df.order_purchase_timestamp, errors="coerce")
    df["record_id"] = df.order_id
    df["date"] = purchased
    df["region"] = df.customer_state.fillna("NI")
    df["category"] = df.product_category_name.fillna("sem_categoria")
    df["channel"] = df.payment_type.fillna("desconhecido")
    df["quantity"] = df.quantity.fillna(0)
    df["unit_value"] = (df.revenue / df.quantity.replace(0, np.nan)).fillna(0)
    df["cost"] = df.freight.fillna(0) / df.quantity.replace(0, np.nan).fillna(1)
    df["engagement"] = (df.installments.fillna(1) * 10).clip(0, 100)
    df["delay_days"] = ((delivered - estimated).dt.total_seconds() / 86400).clip(lower=0).fillna(0)
    df["satisfaction"] = df.satisfaction.fillna(3)
    df["revenue"] = df.payment_value.fillna(df.revenue).fillna(0)
    df["profit"] = df.revenue - df.freight.fillna(0)
    df["target_value"] = df.revenue
    df["target_class"] = (df.delay_days > 0).astype(int)
    if slug == "02_desempenho_logistico":
        df["target_value"] = ((delivered - purchased).dt.total_seconds() / 86400).fillna(0).clip(lower=0)
        df["target_class"] = (df.delay_days > 0).astype(int)
    elif slug == "03_segmentacao_rfm":
        threshold = df.revenue.quantile(.75)
        df["target_class"] = (df.revenue >= threshold).astype(int)
    elif slug == "04_previsao_vendas":
        df["target_value"] = df.revenue
    elif slug == "11_cesta_compras":
        df["target_class"] = (df.seller_count.fillna(1) > 1).astype(int)
    elif slug == "12_voz_cliente":
        df["engagement"] = df.review_text.fillna("").str.len().clip(0, 100)
        df["target_class"] = (df.satisfaction <= 2).astype(int)
    elif slug == "20_pipeline_empresarial":
        df["target_class"] = df.order_status.ne("delivered").astype(int)
    return _finish(df), "Olist Brazilian E-Commerce (Kaggle, dados comerciais anonimizados)"


def load_churn() -> tuple[pd.DataFrame, str]:
    raw = _read_zip("churn.zip", "data_ecommerce_customer_churn.csv")
    df = _base_frame(len(raw))
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["region"] = raw.MaritalStatus
    df["category"] = raw.PreferedOrderCat
    df["channel"] = "E-commerce"
    df["quantity"] = raw.NumberOfDeviceRegistered
    df["unit_value"] = raw.CashbackAmount
    df["cost"] = raw.CashbackAmount
    df["engagement"] = 100 - raw.DaySinceLastOrder.clip(0, 100)
    df["delay_days"] = raw.WarehouseToHome
    df["satisfaction"] = raw.SatisfactionScore
    df["revenue"] = raw.CashbackAmount * 10
    df["profit"] = df.revenue - df.cost
    df["target_class"] = raw.Churn
    df["target_value"] = raw.Tenure
    return _finish(df), "E-commerce Customer Churn (Kaggle)"


def load_marketing(slug: str) -> tuple[pd.DataFrame, str]:
    raw = _read_zip("sales_marketing.zip", "Sales - Marketing customer dataset.csv")
    df = _base_frame(len(raw))
    df["record_id"] = raw.customer_id
    df["date"] = raw.signup_date
    df["region"] = raw.country
    df["category"] = raw.subscription_type
    df["channel"] = raw.acquisition_channel
    df["quantity"] = raw.last_3_month_purchase_freq
    df["unit_value"] = raw.avg_order_value
    df["cost"] = raw.marketing_spend_per_user
    df["engagement"] = raw.email_open_rate * 100
    df["delay_days"] = raw.delivery_delay_days
    df["satisfaction"] = raw.satisfaction_score
    df["revenue"] = raw.total_spent
    df["profit"] = raw.total_spent - raw.marketing_spend_per_user
    df["target_class"] = raw.churn if slug == "06_funil_marketing" else (raw.last_3_month_purchase_freq > raw.last_3_month_purchase_freq.median()).astype(int)
    df["target_value"] = raw.lifetime_value
    return _finish(df), "Sales & Marketing Customer Dataset (Kaggle)"


def load_bank() -> tuple[pd.DataFrame, str]:
    with zipfile.ZipFile(SOURCES / "bank.zip") as outer:
        inner_bytes = outer.read("bank-additional.zip")
    with zipfile.ZipFile(io.BytesIO(inner_bytes)) as inner:
        raw = pd.read_csv(inner.open("bank-additional/bank-additional-full.csv"), sep=";")
    df = _base_frame(len(raw))
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["region"] = raw.marital
    df["category"] = raw.job
    df["channel"] = raw.contact
    df["quantity"] = raw.campaign
    df["unit_value"] = raw.duration
    df["cost"] = raw.campaign
    df["engagement"] = raw.duration.clip(0, 100)
    df["delay_days"] = raw.pdays.replace(999, 0)
    df["satisfaction"] = 3
    df["revenue"] = raw.duration
    df["profit"] = raw.duration - raw.campaign
    df["target_class"] = raw.y.eq("yes").astype(int)
    df["target_value"] = raw.duration
    return _finish(df), "UCI Bank Marketing, DOI 10.24432/C5K306"


def load_fmcg(slug: str) -> tuple[pd.DataFrame, str]:
    raw = _read_zip("fmcg.zip", "fmcg_sales_3years_1M_rows.csv").sample(100_000, random_state=42)
    df = _base_frame(len(raw))
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["date"] = raw.date
    df["region"] = raw.country
    df["category"] = raw.category
    df["channel"] = raw.channel
    df["quantity"] = raw.units_sold
    df["unit_value"] = raw.list_price
    df["cost"] = raw.purchase_cost
    df["engagement"] = raw.discount_pct
    df["delay_days"] = raw.lead_time_days
    df["satisfaction"] = 5 - raw.stock_out_flag * 3
    df["revenue"] = raw.net_sales
    df["profit"] = raw.net_sales - raw.purchase_cost * raw.units_sold
    df["target_class"] = raw.stock_out_flag
    df["target_value"] = raw.units_sold if slug == "10_demanda_estoque" else raw.net_sales
    return _finish(df), "FMCG Multi-Country Sales (Kaggle, amostra determinística de 100 mil linhas)"


def load_hr() -> tuple[pd.DataFrame, str]:
    raw = _read_zip("hr.zip", "WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df = _base_frame(len(raw))
    df["record_id"] = raw.EmployeeNumber
    df["region"] = raw.Department
    df["category"] = raw.JobRole
    df["channel"] = raw.BusinessTravel
    df["quantity"] = raw.YearsAtCompany
    df["unit_value"] = raw.MonthlyIncome
    df["cost"] = raw.DailyRate
    df["engagement"] = raw.JobInvolvement * 25
    df["delay_days"] = raw.DistanceFromHome
    df["satisfaction"] = raw.JobSatisfaction
    df["revenue"] = raw.MonthlyIncome
    df["profit"] = raw.MonthlyIncome - raw.DailyRate
    df["target_class"] = raw.Attrition.eq("Yes").astype(int)
    df["target_value"] = raw.YearsAtCompany
    return _finish(df), "IBM HR Analytics Employee Attrition (Kaggle)"


def load_iranian_churn() -> tuple[pd.DataFrame, str]:
    raw = _read_zip("iranian_churn.zip", "Customer Churn.csv")
    df = _base_frame(len(raw))
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["region"] = raw["Tariff Plan"].astype(str)
    df["category"] = raw["Status"].astype(str)
    df["channel"] = "Telecom"
    df["quantity"] = raw["Frequency of use"]
    df["unit_value"] = raw["Seconds of Use"]
    df["cost"] = raw["Distinct Called Numbers"]
    df["engagement"] = raw["Frequency of SMS"]
    df["delay_days"] = raw["Complains"]
    df["satisfaction"] = 5 - raw["Complains"] * 3
    df["revenue"] = raw["Charge  Amount"]
    df["profit"] = raw["Charge  Amount"] - raw["Complains"]
    df["target_class"] = raw["Churn"]
    df["target_value"] = raw["Customer Value"]
    return _finish(df), "UCI Iranian Churn Dataset, dados reais de uma operadora"


def load_marketing_funnel() -> tuple[pd.DataFrame, str]:
    leads = _read_zip("olist_marketing.zip", "olist_marketing_qualified_leads_dataset.csv")
    deals = _read_zip("olist_marketing.zip", "olist_closed_deals_dataset.csv")
    raw = leads.merge(deals, on="mql_id", how="left")
    df = _base_frame(len(raw))
    df["record_id"] = raw.mql_id
    df["date"] = raw.first_contact_date
    df["region"] = "Brasil"
    df["category"] = raw.landing_page_id.fillna("desconhecida")
    df["channel"] = raw.origin.fillna("desconhecido")
    df["quantity"] = 1
    df["unit_value"] = 0
    df["cost"] = 1
    df["engagement"] = raw.origin.fillna("").str.len() * 5
    df["delay_days"] = 0
    df["satisfaction"] = 3
    df["revenue"] = raw.declared_monthly_revenue.fillna(0)
    df["profit"] = df.revenue - df.cost
    df["target_class"] = raw.won_date.notna().astype(int)
    df["target_value"] = raw.declared_monthly_revenue.fillna(0)
    return _finish(df), "Olist Marketing Funnel (dados comerciais reais anonimizados)"


def load_online_retail(slug: str) -> tuple[pd.DataFrame, str]:
    with zipfile.ZipFile(SOURCES / "online_retail.zip") as archive:
        raw = pd.read_excel(archive.open("Online Retail.xlsx"))
    raw = raw[(raw.Quantity > 0) & (raw.UnitPrice > 0)].sample(min(100_000, len(raw)), random_state=42).reset_index(drop=True)
    df = _base_frame(len(raw))
    df["record_id"] = raw.InvoiceNo.astype(str) + "-" + raw.StockCode.astype(str)
    df["date"] = raw.InvoiceDate
    df["region"] = raw.Country
    df["category"] = raw.Description.fillna("Sem descrição")
    df["channel"] = "Varejo online"
    df["quantity"] = raw.Quantity
    df["unit_value"] = raw.UnitPrice
    df["cost"] = raw.UnitPrice * .65
    df["engagement"] = raw.groupby("CustomerID")["InvoiceNo"].transform("nunique").fillna(1).clip(0, 100)
    df["delay_days"] = 0
    df["satisfaction"] = 4
    df["revenue"] = raw.Quantity * raw.UnitPrice
    df["profit"] = df.revenue - df.cost * raw.Quantity
    df["target_class"] = (raw.Quantity > raw.Quantity.median()).astype(int)
    df["target_value"] = raw.Quantity if slug == "10_demanda_estoque" else df.revenue
    return _finish(df), "UCI Online Retail, transações reais de varejo britânico"


def load_absenteeism() -> tuple[pd.DataFrame, str]:
    raw = _read_zip("absenteeism.zip", "Absenteeism_at_work.csv", sep=";")
    df = _base_frame(len(raw))
    df["record_id"] = raw.ID
    df["date"] = pd.to_datetime(dict(year=2010, month=raw["Month of absence"].clip(1, 12), day=1))
    df["region"] = raw["Reason for absence"].astype(str)
    df["category"] = raw["Education"].astype(str)
    df["channel"] = raw["Seasons"].astype(str)
    df["quantity"] = raw["Service time"]
    df["unit_value"] = raw["Work load Average/day "]
    df["cost"] = raw["Transportation expense"]
    df["engagement"] = (raw["Service time"] * 5).clip(0, 100)
    df["delay_days"] = raw["Distance from Residence to Work"]
    df["satisfaction"] = 3
    df["revenue"] = raw["Work load Average/day "]
    df["profit"] = df.revenue - df.cost
    df["target_class"] = (raw["Absenteeism time in hours"] > raw["Absenteeism time in hours"].median()).astype(int)
    df["target_value"] = raw["Absenteeism time in hours"]
    return _finish(df), "UCI Absenteeism at Work, registros reais de uma empresa brasileira"


def load_bcb() -> tuple[pd.DataFrame, str]:
    raw = pd.read_csv(SOURCES / "bcb_inadimplencia.csv", sep=";", decimal=",")
    df = _base_frame(len(raw))
    value = pd.to_numeric(raw.valor.astype(str).str.replace(",", "."), errors="coerce")
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["date"] = pd.to_datetime(raw.data, dayfirst=True)
    df["region"] = "Brasil"
    df["category"] = "Carteira de crédito"
    df["channel"] = "Sistema Financeiro Nacional"
    df["quantity"] = 1
    df["unit_value"] = value
    df["engagement"] = value
    df["satisfaction"] = (5 - value / 2).clip(1, 5)
    df["revenue"] = value
    df["profit"] = -value
    df["target_class"] = (value > value.median()).astype(int)
    df["target_value"] = value
    return _finish(df), "Banco Central do Brasil, SGS série 21082"


def load_taxi() -> tuple[pd.DataFrame, str]:
    raw = pd.read_parquet(SOURCES / "nyc_taxi_2025_01.parquet").sample(100_000, random_state=42).reset_index(drop=True)
    df = _base_frame(len(raw))
    df["record_id"] = np.arange(1, len(raw) + 1)
    df["date"] = raw.tpep_pickup_datetime
    df["region"] = raw.PULocationID.astype(str)
    df["category"] = raw.RatecodeID.astype(str)
    df["channel"] = raw.payment_type.astype(str)
    df["quantity"] = raw.passenger_count.fillna(1)
    df["unit_value"] = raw.fare_amount
    df["cost"] = raw.tolls_amount
    df["engagement"] = raw.trip_distance
    df["delay_days"] = (pd.to_datetime(raw.tpep_dropoff_datetime) - pd.to_datetime(raw.tpep_pickup_datetime)).dt.total_seconds() / 60
    df["satisfaction"] = 4
    df["revenue"] = raw.total_amount
    df["profit"] = raw.fare_amount - raw.tolls_amount
    df["target_class"] = (raw.tip_amount > 0).astype(int)
    df["target_value"] = raw.total_amount
    return _finish(df), "NYC TLC Yellow Taxi Trip Records, janeiro de 2025"


def load_citibike() -> tuple[pd.DataFrame, str]:
    raw = _read_zip("citibike.zip", "JC-202501-citibike-tripdata.csv")
    duration = (pd.to_datetime(raw.ended_at) - pd.to_datetime(raw.started_at)).dt.total_seconds() / 60
    df = _base_frame(len(raw))
    df["record_id"] = raw.ride_id
    df["date"] = raw.started_at
    df["region"] = raw.start_station_name.fillna("Sem estação")
    df["category"] = raw.rideable_type
    df["channel"] = raw.member_casual
    df["quantity"] = 1
    df["unit_value"] = duration
    df["cost"] = duration * .05
    df["engagement"] = duration.clip(0, 100)
    df["delay_days"] = duration
    df["satisfaction"] = 4
    df["revenue"] = duration * .2
    df["profit"] = df.revenue - df.cost
    df["target_class"] = raw.member_casual.eq("member").astype(int)
    df["target_value"] = duration
    return _finish(df), "Citi Bike System Data, Jersey City, janeiro de 2025"


def load_worldbank_health() -> tuple[pd.DataFrame, str]:
    import json
    payload = json.loads((SOURCES / "worldbank_mortality.json").read_text(encoding="utf-8-sig"))[1]
    raw = pd.DataFrame(payload).dropna(subset=["value"])
    value = pd.to_numeric(raw.value)
    df = _base_frame(len(raw))
    df["record_id"] = raw.date
    df["date"] = pd.to_datetime(raw.date + "-01-01")
    df["region"] = "Brasil"
    df["category"] = "Mortalidade infantil"
    df["channel"] = "World Bank"
    df["quantity"] = 1
    df["unit_value"] = value
    df["engagement"] = (100 - value).clip(0, 100)
    df["satisfaction"] = (5 - value / 20).clip(1, 5)
    df["revenue"] = value
    df["profit"] = -value
    df["target_class"] = (value > value.median()).astype(int)
    df["target_value"] = value
    return _finish(df), "World Bank API, mortalidade infantil no Brasil (SH.DYN.MORT)"


def load_credit_default() -> tuple[pd.DataFrame, str]:
    with zipfile.ZipFile(SOURCES / "credit_default.zip") as archive:
        raw = pd.read_excel(archive.open("default of credit card clients.xls"), header=1)
    target = raw.iloc[:, -1]
    df = _base_frame(len(raw))
    df["record_id"] = raw.iloc[:, 0]
    df["region"] = raw.SEX.astype(str)
    df["category"] = raw.EDUCATION.astype(str)
    df["channel"] = raw.MARRIAGE.astype(str)
    df["quantity"] = raw.AGE
    df["unit_value"] = raw.LIMIT_BAL
    df["cost"] = raw.PAY_AMT1
    df["engagement"] = raw.PAY_AMT1 / raw.LIMIT_BAL.replace(0, np.nan) * 100
    df["delay_days"] = raw.PAY_0.clip(lower=0)
    df["satisfaction"] = (5 - df.delay_days).clip(1, 5)
    df["revenue"] = raw.LIMIT_BAL
    df["profit"] = raw.PAY_AMT1 - raw.BILL_AMT1
    df["target_class"] = target
    df["target_value"] = raw.BILL_AMT1
    return _finish(df), "UCI Default of Credit Card Clients, DOI 10.24432/C55S3H"


def load_real_data(slug: str) -> tuple[pd.DataFrame, str]:
    if slug in {"01_ecommerce_360", "02_desempenho_logistico", "03_segmentacao_rfm", "04_previsao_vendas", "08_rentabilidade_comercial", "11_cesta_compras", "12_voz_cliente", "20_pipeline_empresarial"}:
        return load_olist(slug)
    if slug == "05_churn_clientes":
        return load_iranian_churn()
    if slug in {"06_funil_marketing", "17_analytics_digital"}:
        return load_marketing_funnel()
    if slug == "07_propensao_compra":
        return load_bank()
    if slug in {"09_elasticidade_preco", "10_demanda_estoque"}:
        return load_online_retail(slug)
    if slug == "13_people_analytics":
        return load_absenteeism()
    if slug == "14_inadimplencia":
        return load_bcb()
    if slug == "15_mobilidade_urbana":
        return load_taxi()
    if slug == "16_bicicletas_compartilhadas":
        return load_citibike()
    if slug == "18_saude_publica":
        return load_worldbank_health()
    if slug == "19_anomalias_financeiras":
        return load_credit_default()
    raise KeyError(f"Fonte real ainda não configurada: {slug}")
