from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = "data/processed/analytics.csv"

SQL = {
"01_ecommerce_360": """-- Receita, resultado e atraso por estado e categoria
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
performance AS (
 SELECT region, category, COUNT(*) pedidos, SUM(revenue) receita, SUM(profit) resultado,
        AVG(satisfaction) satisfacao_media, AVG(target_class) taxa_atraso
 FROM base GROUP BY region, category)
SELECT *, ROUND(100*resultado/NULLIF(receita,0),2) margem_pct,
       DENSE_RANK() OVER(ORDER BY resultado DESC) ranking_resultado
FROM performance ORDER BY ranking_resultado;
""",
"02_desempenho_logistico": """-- SLA logístico e efeito do atraso na satisfação
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT region, CASE WHEN delay_days=0 THEN 'no_prazo' WHEN delay_days<=3 THEN '1_3_dias' ELSE 'acima_3_dias' END faixa_atraso,
        COUNT(*) pedidos, AVG(target_value) tempo_total_medio, AVG(satisfaction) satisfacao_media
 FROM base GROUP BY region, faixa_atraso)
SELECT *, ROUND(100*pedidos/SUM(pedidos) OVER(PARTITION BY region),2) participacao_pct
FROM faixas ORDER BY region, faixa_atraso;
""",
"03_segmentacao_rfm": """-- Segmentação de valor baseada no comportamento observado
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
score AS (
 SELECT record_id, region, revenue, satisfaction, delay_days,
        NTILE(4) OVER(ORDER BY revenue) quartil_valor
 FROM base)
SELECT quartil_valor, COUNT(*) clientes, AVG(revenue) receita_media,
       AVG(satisfaction) satisfacao_media, AVG(delay_days) atraso_medio
FROM score GROUP BY quartil_valor ORDER BY quartil_valor DESC;
""",
"04_previsao_vendas": """-- Série mensal e média móvel para planejamento de vendas
WITH mensal AS (
 SELECT month, SUM(revenue) receita FROM read_csv_auto('data/processed/analytics.csv') GROUP BY month)
SELECT month, receita, LAG(receita) OVER(ORDER BY month) receita_anterior,
       AVG(receita) OVER(ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) media_movel_3m,
       ROUND(100*(receita-LAG(receita) OVER(ORDER BY month))/NULLIF(LAG(receita) OVER(ORDER BY month),0),2) variacao_pct
FROM mensal ORDER BY month;
""",
"05_churn_clientes": """-- Churn por plano e intensidade de uso
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
segmentos AS (
 SELECT region plano, CASE WHEN engagement<25 THEN 'baixo' WHEN engagement<60 THEN 'medio' ELSE 'alto' END uso,
        COUNT(*) clientes, SUM(target_class) churns, AVG(target_value) valor_medio
 FROM base GROUP BY plano, uso)
SELECT *, ROUND(100.0*churns/NULLIF(clientes,0),2) churn_pct
FROM segmentos ORDER BY churn_pct DESC;
""",
"06_funil_marketing": """-- Conversão de leads por origem e landing page
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
funil AS (
 SELECT channel origem, category landing_page, COUNT(*) leads, SUM(target_class) negocios,
        SUM(revenue) receita_declarada
 FROM base GROUP BY origem, landing_page)
SELECT *, ROUND(100.0*negocios/NULLIF(leads,0),2) conversao_pct,
       RANK() OVER(PARTITION BY origem ORDER BY negocios DESC) ranking_landing
FROM funil WHERE leads>=5 ORDER BY conversao_pct DESC;
""",
"07_propensao_compra": """-- Propensão observada por perfil e histórico de contato
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category ocupacao, channel contato, COUNT(*) clientes, SUM(target_class) conversoes,
       ROUND(100*AVG(target_class),2) conversao_pct, AVG(quantity) contatos_medios,
       AVG(delay_days) dias_desde_contato_anterior
FROM base GROUP BY ocupacao, contato HAVING COUNT(*)>=30 ORDER BY conversao_pct DESC;
""",
"08_rentabilidade_comercial": """-- Categorias com receita alta e resultado insuficiente
WITH categorias AS (
 SELECT category, COUNT(*) pedidos, SUM(revenue) receita, SUM(profit) resultado
 FROM read_csv_auto('data/processed/analytics.csv') GROUP BY category)
SELECT *, ROUND(100*resultado/NULLIF(receita,0),2) margem_pct,
       CASE WHEN resultado<0 THEN 'rever' WHEN resultado/NULLIF(receita,0)<0.15 THEN 'atencao' ELSE 'saudavel' END status
FROM categorias ORDER BY resultado ASC;
""",
"09_elasticidade_preco": """-- Relação entre faixa de preço e unidades vendidas
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT category, NTILE(5) OVER(PARTITION BY category ORDER BY unit_value) faixa_preco,
        unit_value, quantity, revenue FROM base)
SELECT category, faixa_preco, COUNT(*) transacoes, AVG(unit_value) preco_medio,
       AVG(quantity) quantidade_media, SUM(revenue) receita
FROM faixas GROUP BY category, faixa_preco HAVING COUNT(*)>=10 ORDER BY category, faixa_preco;
""",
"10_demanda_estoque": """-- Demanda mensal e volatilidade por produto
WITH mensal AS (
 SELECT month, category, SUM(quantity) demanda FROM read_csv_auto('data/processed/analytics.csv') GROUP BY month, category),
stats AS (
 SELECT category, AVG(demanda) demanda_media, STDDEV_SAMP(demanda) volatilidade, MAX(demanda) pico
 FROM mensal GROUP BY category)
SELECT *, ROUND(volatilidade/NULLIF(demanda_media,0),3) coef_variacao,
       RANK() OVER(ORDER BY volatilidade DESC) ranking_risco
FROM stats ORDER BY ranking_risco;
""",
"11_cesta_compras": """-- Pedidos com múltiplos vendedores como proxy de cesta complexa
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category, COUNT(*) pedidos, SUM(target_class) cestas_multivendedor,
       ROUND(100*AVG(target_class),2) cesta_complexa_pct, AVG(quantity) itens_medios,
       AVG(revenue) ticket_medio
FROM base GROUP BY category HAVING COUNT(*)>=20 ORDER BY cesta_complexa_pct DESC;
""",
"12_voz_cliente": """-- Insatisfação por categoria, atraso e tamanho do comentário
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT category, CASE WHEN delay_days=0 THEN 'no_prazo' ELSE 'atrasado' END entrega,
       COUNT(*) avaliacoes, ROUND(100*AVG(target_class),2) negativas_pct,
       AVG(engagement) tamanho_comentario, AVG(satisfaction) nota_media
FROM base GROUP BY category, entrega HAVING COUNT(*)>=20 ORDER BY negativas_pct DESC;
""",
"13_people_analytics": """-- Absenteísmo por motivo, escolaridade e tempo de serviço
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region motivo, category escolaridade, COUNT(*) registros,
       AVG(target_value) horas_ausencia, ROUND(100*AVG(target_class),2) ausencia_alta_pct,
       AVG(quantity) tempo_servico
FROM base GROUP BY motivo, escolaridade HAVING COUNT(*)>=5 ORDER BY horas_ausencia DESC;
""",
"14_inadimplencia": """-- Tendência da inadimplência da carteira de crédito
WITH serie AS (
 SELECT date, target_value inadimplencia,
        LAG(target_value,12) OVER(ORDER BY date) valor_12m_atras FROM read_csv_auto('data/processed/analytics.csv'))
SELECT date, inadimplencia, valor_12m_atras,
       ROUND(inadimplencia-valor_12m_atras,2) variacao_pp_12m,
       AVG(inadimplencia) OVER(ORDER BY date ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) media_movel_6m
FROM serie ORDER BY date;
""",
"15_mobilidade_urbana": """-- Corridas, duração e valor por zona e hora
WITH base AS (SELECT *, EXTRACT(hour FROM date) hora FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region zona_origem, hora, COUNT(*) corridas, AVG(quantity) passageiros,
       AVG(engagement) distancia_media, AVG(target_value) duracao_media_min,
       AVG(revenue) valor_medio
FROM base GROUP BY zona_origem, hora HAVING COUNT(*)>=10 ORDER BY corridas DESC;
""",
"16_bicicletas_compartilhadas": """-- Fluxo de viagens por estação, hora e tipo de usuário
WITH base AS (SELECT *, EXTRACT(hour FROM date) hora FROM read_csv_auto('data/processed/analytics.csv'))
SELECT region estacao_origem, hora, channel tipo_usuario, COUNT(*) viagens,
       AVG(target_value) duracao_media_min,
       RANK() OVER(PARTITION BY hora ORDER BY COUNT(*) DESC) ranking_estacao
FROM base GROUP BY estacao_origem, hora, tipo_usuario ORDER BY viagens DESC;
""",
"17_analytics_digital": """-- Desempenho de origens e landing pages no funil digital
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv'))
SELECT channel origem, category landing_page, COUNT(*) sessoes_qualificadas,
       SUM(target_class) conversoes, ROUND(100*AVG(target_class),2) taxa_conversao,
       SUM(revenue) valor_declarado
FROM base GROUP BY origem, landing_page HAVING COUNT(*)>=5 ORDER BY taxa_conversao DESC;
""",
"18_saude_publica": """-- Evolução da mortalidade infantil no Brasil
WITH serie AS (
 SELECT date, target_value taxa, LAG(target_value) OVER(ORDER BY date) taxa_anterior
 FROM read_csv_auto('data/processed/analytics.csv'))
SELECT date, taxa, taxa_anterior, ROUND(taxa-taxa_anterior,2) variacao_anual,
       ROUND(100*(taxa-taxa_anterior)/NULLIF(taxa_anterior,0),2) variacao_pct
FROM serie ORDER BY date;
""",
"19_anomalias_financeiras": """-- Risco de inadimplência por limite, perfil e atraso prévio
WITH base AS (SELECT * FROM read_csv_auto('data/processed/analytics.csv')),
faixas AS (
 SELECT *, NTILE(5) OVER(ORDER BY unit_value) faixa_limite FROM base)
SELECT faixa_limite, region sexo, category escolaridade, COUNT(*) clientes,
       ROUND(100*AVG(target_class),2) default_pct, AVG(unit_value) limite_medio,
       AVG(delay_days) atraso_previo
FROM faixas GROUP BY faixa_limite, sexo, escolaridade ORDER BY default_pct DESC;
""",
"20_pipeline_empresarial": """-- Contrato de qualidade e reconciliação da camada analítica
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
""",
}

for slug, sql in SQL.items():
    (ROOT / "projetos" / slug / "analysis.sql").write_text(sql, encoding="utf-8")
print(f"{len(SQL)} análises SQL especializadas.")
