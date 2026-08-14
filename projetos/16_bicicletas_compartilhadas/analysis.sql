-- Fluxo de viagens por estação, hora e tipo de usuário
WITH base AS (SELECT *, EXTRACT(hour FROM date) hora FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region estacao_origem, hora, channel tipo_usuario, COUNT(*) viagens,
       AVG(target_value) duracao_media_min,
       RANK() OVER(PARTITION BY hora ORDER BY COUNT(*) DESC) ranking_estacao
FROM base GROUP BY estacao_origem, hora, tipo_usuario ORDER BY viagens DESC;
