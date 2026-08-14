-- Contrato de qualidade e reconciliação da camada analítica
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
checks AS (
 SELECT COUNT(*) linhas, COUNT(DISTINCT record_id) ids_unicos,
        SUM(CASE WHEN record_id IS NULL THEN 1 ELSE 0 END) ids_nulos,
        SUM(CASE WHEN revenue<0 THEN 1 ELSE 0 END) receitas_negativas,
        SUM(revenue) receita, SUM(profit) resultado, MAX(date) data_maxima
 FROM base)
SELECT *, linhas-ids_unicos duplicidades,
       CASE WHEN ids_nulos=0 AND receitas_negativas=0 THEN 'aprovado' ELSE 'bloqueado' END status_publicacao
FROM checks;
