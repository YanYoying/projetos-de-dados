-- Categorias com receita alta e resultado insuficiente
WITH categorias AS (
 SELECT category, COUNT(*) pedidos, SUM(revenue) receita, SUM(profit) resultado
 FROM read_csv_auto('data/processed/analytics.csv') GROUP BY category)
SELECT *, ROUND(100*resultado/NULLIF(receita,0),2) margem_pct,
       CASE WHEN resultado<0 THEN 'rever' WHEN resultado/NULLIF(receita,0)<0.15 THEN 'atencao' ELSE 'saudavel' END status
FROM categorias ORDER BY resultado ASC;
