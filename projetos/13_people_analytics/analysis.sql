-- Absenteísmo por motivo, escolaridade e tempo de serviço
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region motivo, category escolaridade, COUNT(*) registros,
       AVG(target_value) horas_ausencia, ROUND(100*AVG(target_class),2) ausencia_alta_pct,
       AVG(quantity) tempo_servico
FROM base GROUP BY motivo, escolaridade HAVING COUNT(*)>=5 ORDER BY horas_ausencia DESC;
