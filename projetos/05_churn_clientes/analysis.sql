-- Análise executiva avançada: CTEs, janela, ranking e variação temporal
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
