from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROJECTS = [
    ("01_ecommerce_360", "E-commerce 360°", "Quais produtos, vendedores e regiões sustentam receita, margem e satisfação?", "regression", "Olist", "Concentrar investimento nas combinações de categoria e região com margem positiva e alta satisfação."),
    ("02_desempenho_logistico", "Desempenho logístico", "Onde estão os atrasos e como eles afetam satisfação e recompra?", "regression", "Olist", "Priorizar rotas com alto volume, atraso acima do SLA e queda de satisfação."),
    ("03_segmentacao_rfm", "Segmentação RFM", "Quais clientes são valiosos, promissores ou estão em risco?", "classification", "Olist", "Aplicar campanhas distintas para clientes VIP, promissores e em risco."),
    ("04_previsao_vendas", "Previsão de vendas", "Quanto será vendido por período, categoria e região?", "regression", "Olist", "Usar a previsão para ajustar metas, compras e capacidade operacional."),
    ("05_churn_clientes", "Churn de clientes", "Quais clientes têm maior risco de abandonar a empresa?", "classification", "Kaggle E-commerce Churn", "Acionar retenção apenas quando valor esperado superar o custo do incentivo."),
    ("06_funil_marketing", "Funil de marketing", "Quais canais entregam conversão e retorno sobre investimento?", "classification", "Kaggle Sales & Marketing", "Realocar verba de canais com CAC alto para canais de maior conversão e LTV."),
    ("07_propensao_compra", "Propensão à compra", "Quem tem maior chance de aceitar uma oferta?", "classification", "UCI Bank Marketing", "Ordenar contatos por propensão e limitar campanhas de baixo retorno."),
    ("08_rentabilidade_comercial", "Rentabilidade comercial", "Quais produtos vendem muito, mas reduzem a margem?", "regression", "Tableau Superstore", "Rever descontos de itens com grande receita e lucro baixo ou negativo."),
    ("09_elasticidade_preco", "Elasticidade de preço", "Como preço e promoção alteram demanda e margem?", "regression", "Kaggle FMCG", "Testar faixas de preço que maximizem margem, não apenas volume."),
    ("10_demanda_estoque", "Demanda e estoque", "Quais itens correm risco de ruptura ou excesso?", "regression", "Kaggle FMCG", "Definir estoque de segurança por volatilidade e tempo de reposição."),
    ("11_cesta_compras", "Cesta de compras", "Quais produtos apresentam maior afinidade de compra?", "classification", "Olist", "Criar combos somente quando lift e margem incremental forem positivos."),
    ("12_voz_cliente", "Voz do cliente", "Quais causas estão associadas às avaliações negativas?", "classification", "Olist Reviews", "Atacar os temas recorrentes com maior impacto em satisfação e receita."),
    ("13_people_analytics", "People Analytics", "Quais fatores estão associados à saída de funcionários?", "classification", "IBM HR Attrition", "Usar o risco para orientar diagnóstico humano, nunca decisões automáticas de desligamento."),
    ("14_inadimplencia", "Inadimplência", "Como o risco da carteira evolui ao longo do tempo?", "regression", "Banco Central do Brasil", "Ajustar provisões e políticas quando tendência e cenário macro indicarem deterioração."),
    ("15_mobilidade_urbana", "Mobilidade urbana", "Onde e quando existe maior demanda por transporte?", "regression", "NYC TLC", "Reposicionar oferta para zonas e horários de demanda recorrente."),
    ("16_bicicletas_compartilhadas", "Bicicletas compartilhadas", "Quais estações precisam de rebalanceamento?", "regression", "BigQuery Citi Bike", "Rebalancear estações antes dos picos previstos, minimizando viagens operacionais."),
    ("17_analytics_digital", "Analytics digital", "Quais canais e páginas contribuem para conversão?", "classification", "Google Analytics Sample", "Otimizar etapas com maior abandono e avaliar canais por receita incremental."),
    ("18_saude_publica", "Saúde pública", "Quais territórios e grupos precisam de maior atenção?", "regression", "Dados Abertos do SUS", "Priorizar investigação territorial com taxas ajustadas por população."),
    ("19_anomalias_financeiras", "Anomalias financeiras", "Quais transações apresentam comportamento suspeito?", "classification", "UCI/Kaggle", "Revisar alertas por risco e valor, calibrando o custo de falsos positivos."),
    ("20_pipeline_empresarial", "Pipeline empresarial", "Como entregar indicadores confiáveis e atualizados?", "classification", "Olist SQLite", "Monitorar qualidade, linhagem e atualização antes de publicar indicadores."),
]

SQL = """-- Análise executiva avançada: CTEs, janela, ranking e variação temporal
WITH monthly AS (
    SELECT month, region, category,
           SUM(revenue) AS revenue, SUM(profit) AS profit,
           AVG(satisfaction) AS satisfaction
    FROM read_csv_auto('data/processed/analytics.csv')
    GROUP BY month, region, category
), trends AS (
    SELECT *,
           LAG(revenue) OVER (PARTITION BY region, category ORDER BY month) AS previous_revenue,
           RANK() OVER (PARTITION BY month ORDER BY profit DESC) AS profit_rank
    FROM monthly
)
SELECT *,
       ROUND(100 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0), 2) AS revenue_growth_pct,
       ROUND(100 * profit / NULLIF(revenue, 0), 2) AS margin_pct
FROM trends
ORDER BY month DESC, profit_rank;
"""

PIPELINE = """from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[2]
path.insert(0, str(ROOT))
from src.portfolio_core import run_pipeline

if __name__ == '__main__':
    print(run_pipeline(Path(__file__).resolve().parent))
"""

MODEL = """from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[2]
path.insert(0, str(ROOT))
from src.portfolio_core import train_model

if __name__ == '__main__':
    print(train_model(Path(__file__).resolve().parent))
"""

DASHBOARD = """from pathlib import Path
from sys import path

ROOT = Path(__file__).resolve().parents[2]
path.insert(0, str(ROOT))
from src.portfolio_core import render_dashboard

render_dashboard(Path(__file__).resolve().parent)
"""


def main() -> None:
    for index, (slug, title, question, model_type, source, recommendation) in enumerate(PROJECTS, 1):
        folder = ROOT / "projetos" / slug
        folder.mkdir(parents=True, exist_ok=True)
        config = {
            "title": title, "business_question": question, "model_type": model_type,
            "source": source, "seed": 100 + index, "target_label": "Taxa do indicador",
            "recommendation": recommendation,
        }
        (folder / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        (folder / "pipeline.py").write_text(PIPELINE, encoding="utf-8")
        (folder / "model.py").write_text(MODEL, encoding="utf-8")
        (folder / "dashboard.py").write_text(DASHBOARD, encoding="utf-8")
        (folder / "analysis.sql").write_text(SQL, encoding="utf-8")
        readme = f"""# {title}\n\n## Problema de negócio\n\n{question}\n\n## Entregáveis\n\n- `dashboard.py`: visão executiva e filtros interativos.\n- `analysis.sql`: CTEs, funções de janela, ranking, crescimento e margem.\n- `model.py`: modelo preditivo e métricas reproduzíveis.\n- `pipeline.py`: ETL com validação e camada analítica.\n\n## Fonte recomendada\n\n{source}. A execução inicial usa dados sintéticos determinísticos; substitua a etapa de extração pela base indicada mantendo o contrato da camada processada.\n\n## Recomendação executiva\n\n{recommendation}\n\n## Como executar\n\n```powershell\npython pipeline.py\npython model.py\nstreamlit run dashboard.py\n```\n"""
        (folder / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()

