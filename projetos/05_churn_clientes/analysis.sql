-- Churn por plano e intensidade de uso
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
segmentos AS (
 SELECT region plano, CASE WHEN engagement<25 THEN 'baixo' WHEN engagement<60 THEN 'medio' ELSE 'alto' END uso,
        COUNT(*) clientes, SUM(target_class) churns, AVG(target_value) valor_medio
 FROM base GROUP BY plano, uso)
SELECT *, ROUND(100.0*churns/NULLIF(clientes,0),2) churn_pct
FROM segmentos ORDER BY churn_pct DESC;
