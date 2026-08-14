-- Evolução da mortalidade infantil no Brasil
WITH serie AS (
 SELECT date, target_value taxa, LAG(target_value) OVER(ORDER BY date) taxa_anterior
 FROM read_csv_auto('data/processed/analytics.csv'))
SELECT date, taxa, taxa_anterior, ROUND(taxa-taxa_anterior,2) variacao_anual,
       ROUND(100*(taxa-taxa_anterior)/NULLIF(taxa_anterior,0),2) variacao_pct
FROM serie ORDER BY date;
