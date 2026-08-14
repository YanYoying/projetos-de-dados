-- Demanda mensal e volatilidade por produto
WITH mensal AS (
 SELECT month, category, SUM(quantity) demanda FROM read_csv_auto('data/processed/analytics.csv') GROUP BY month, category),
stats AS (
 SELECT category, AVG(demanda) demanda_media, STDDEV_SAMP(demanda) volatilidade, MAX(demanda) pico
 FROM mensal GROUP BY category)
SELECT *, ROUND(volatilidade/NULLIF(demanda_media,0),3) coef_variacao,
       RANK() OVER(ORDER BY volatilidade DESC) ranking_risco
FROM stats ORDER BY ranking_risco;
