-- Receita, resultado e atraso por estado e categoria
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
performance AS (
 SELECT region, category, COUNT(*) pedidos, SUM(revenue) receita, SUM(profit) resultado,
        AVG(satisfaction) satisfacao_media, AVG(target_class) taxa_atraso
 FROM base GROUP BY region, category)
SELECT *, ROUND(100*resultado/NULLIF(receita,0),2) margem_pct,
       DENSE_RANK() OVER(ORDER BY resultado DESC) ranking_resultado
FROM performance ORDER BY ranking_resultado;
