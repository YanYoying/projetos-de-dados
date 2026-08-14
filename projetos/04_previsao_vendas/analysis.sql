-- Série mensal e média móvel para planejamento de vendas
WITH mensal AS (
 SELECT month, SUM(revenue) receita FROM read_csv_auto('data/processed/analytics.csv') GROUP BY month)
SELECT month, receita, LAG(receita) OVER(ORDER BY month) receita_anterior,
       AVG(receita) OVER(ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) media_movel_3m,
       ROUND(100*(receita-LAG(receita) OVER(ORDER BY month))/NULLIF(LAG(receita) OVER(ORDER BY month),0),2) variacao_pct
FROM mensal ORDER BY month;
