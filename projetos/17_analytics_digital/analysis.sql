-- Desempenho de origens e landing pages no funil digital
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT channel origem, category landing_page, COUNT(*) sessoes_qualificadas,
       SUM(target_class) conversoes, ROUND(100*AVG(target_class),2) taxa_conversao,
       SUM(revenue) valor_declarado
FROM base GROUP BY origem, landing_page HAVING COUNT(*)>=5 ORDER BY taxa_conversao DESC;
