-- Segmentação de valor baseada no comportamento observado
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
score AS (
 SELECT record_id, region, revenue, satisfaction, delay_days,
        NTILE(4) OVER(ORDER BY revenue) quartil_valor
 FROM base)
SELECT quartil_valor, COUNT(*) clientes, AVG(revenue) receita_media,
       AVG(satisfaction) satisfacao_media, AVG(delay_days) atraso_medio
FROM score GROUP BY quartil_valor ORDER BY quartil_valor DESC;
