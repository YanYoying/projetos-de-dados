-- SLA logístico e efeito do atraso na satisfação
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT region, CASE WHEN delay_days=0 THEN 'no_prazo' WHEN delay_days<=3 THEN '1_3_dias' ELSE 'acima_3_dias' END faixa_atraso,
        COUNT(*) pedidos, AVG(target_value) tempo_total_medio, AVG(satisfaction) satisfacao_media
 FROM base GROUP BY region, faixa_atraso)
SELECT *, ROUND(100*pedidos/SUM(pedidos) OVER(PARTITION BY region),2) participacao_pct
FROM faixas ORDER BY region, faixa_atraso;
