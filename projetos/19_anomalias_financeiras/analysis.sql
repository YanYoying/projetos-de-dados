-- Risco de inadimplência por limite, perfil e atraso prévio
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT *, NTILE(5) OVER(ORDER BY unit_value) faixa_limite FROM base)
SELECT faixa_limite, region sexo, category escolaridade, COUNT(*) clientes,
       ROUND(100*AVG(target_class),2) default_pct, AVG(unit_value) limite_medio,
       AVG(delay_days) atraso_previo
FROM faixas GROUP BY faixa_limite, sexo, escolaridade ORDER BY default_pct DESC;
