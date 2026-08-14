-- Corridas, duração e valor por zona e hora
WITH base AS (SELECT *, EXTRACT(hour FROM date) hora FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region zona_origem, hora, COUNT(*) corridas, AVG(quantity) passageiros,
       AVG(engagement) distancia_media, AVG(target_value) duracao_media_min,
       AVG(revenue) valor_medio
FROM base GROUP BY zona_origem, hora HAVING COUNT(*)>=10 ORDER BY corridas DESC;
