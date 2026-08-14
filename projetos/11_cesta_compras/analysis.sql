-- Pedidos com múltiplos vendedores como proxy de cesta complexa
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category, COUNT(*) pedidos, SUM(target_class) cestas_multivendedor,
       ROUND(100*AVG(target_class),2) cesta_complexa_pct, AVG(quantity) itens_medios,
       AVG(revenue) ticket_medio
FROM base GROUP BY category HAVING COUNT(*)>=20 ORDER BY cesta_complexa_pct DESC;
