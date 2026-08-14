-- Propensão observada por perfil e histórico de contato
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category ocupacao, channel contato, COUNT(*) clientes, SUM(target_class) conversoes,
       ROUND(100*AVG(target_class),2) conversao_pct, AVG(quantity) contatos_medios,
       AVG(delay_days) dias_desde_contato_anterior
FROM base GROUP BY ocupacao, contato HAVING COUNT(*)>=30 ORDER BY conversao_pct DESC;
