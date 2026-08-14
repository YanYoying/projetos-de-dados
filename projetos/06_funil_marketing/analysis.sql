-- Conversão de leads por origem e landing page
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
funil AS (
 SELECT channel origem, category landing_page, COUNT(*) leads, SUM(target_class) negocios,
        SUM(revenue) receita_declarada
 FROM base GROUP BY origem, landing_page)
SELECT *, ROUND(100.0*negocios/NULLIF(leads,0),2) conversao_pct,
       RANK() OVER(PARTITION BY origem ORDER BY negocios DESC) ranking_landing
FROM funil WHERE leads>=5 ORDER BY conversao_pct DESC;
