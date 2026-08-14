-- Relação entre faixa de preço e unidades vendidas
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT category, NTILE(5) OVER(PARTITION BY category ORDER BY unit_value) faixa_preco,
        unit_value, quantity, revenue FROM base)
SELECT category, faixa_preco, COUNT(*) transacoes, AVG(unit_value) preco_medio,
       AVG(quantity) quantidade_media, SUM(revenue) receita
FROM faixas GROUP BY category, faixa_preco HAVING COUNT(*)>=10 ORDER BY category, faixa_preco;
