-- Tendência da inadimplência da carteira de crédito
WITH serie AS (
 SELECT date, target_value inadimplencia,
        LAG(target_value,12) OVER(ORDER BY date) valor_12m_atras FROM read_csv_auto('data/processed/analytics.csv'))
SELECT date, inadimplencia, valor_12m_atras,
       ROUND(inadimplencia-valor_12m_atras,2) variacao_pp_12m,
       AVG(inadimplencia) OVER(ORDER BY date ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) media_movel_6m
FROM serie ORDER BY date;
