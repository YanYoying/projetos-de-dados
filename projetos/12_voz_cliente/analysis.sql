-- Insatisfação por categoria, atraso e tamanho do comentário
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category, CASE WHEN delay_days=0 THEN 'no_prazo' ELSE 'atrasado' END entrega,
       COUNT(*) avaliacoes, ROUND(100*AVG(target_class),2) negativas_pct,
       AVG(engagement) tamanho_comentario, AVG(satisfaction) nota_media
FROM base GROUP BY category, entrega HAVING COUNT(*)>=20 ORDER BY negativas_pct DESC;
