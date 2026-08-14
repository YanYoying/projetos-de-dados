# Guia de entrevista — Analista de Dados Júnior

## Apresentação de 60 segundos

“Construí um portfólio com dados públicos reais cobrindo varejo, marketing, retenção e operações. Nos projetos principais, criei pipelines de tratamento, análises SQL com funções de janela, dashboards executivos e modelos preditivos avaliados fora da amostra. Meu foco foi transformar métricas em decisões e documentar limitações, não apenas produzir gráficos.”

## Perguntas que você deve saber responder

### E-commerce 360°

- Por que receita não é suficiente para avaliar uma categoria?
- Como o frete foi incorporado ao resultado?
- Como um pedido com vários itens altera a granularidade da tabela?
- O que você faria antes de recomendar investimento em uma região?

### Churn

- Por que ROC AUC é útil quando as classes são desbalanceadas?
- Qual é o custo de falso positivo e falso negativo?
- Como evitar vazamento de dados entre treino e teste?
- Como transformar probabilidade de churn em uma ação economicamente viável?

### Funil de marketing

- Qual a diferença entre conversão, CAC, ROI e LTV?
- Por que atributos registrados depois do fechamento não podem prever o fechamento?
- Como você testaria se um canal realmente causa mais conversões?

### Demanda e estoque

- Por que a divisão aleatória pode ser inadequada para séries temporais?
- Como calcular estoque de segurança?
- O que MAE representa para o negócio?

### Pipeline empresarial

- Qual a diferença entre camada bruta, tratada e analítica?
- Quais testes impediriam a publicação de dados incorretos?
- Como garantir reprocessamento idempotente?
- Por que os arquivos brutos não estão no Git?

## Limitações que devem ser mencionadas

- Algumas fontes são históricas e não representam o mercado atual.
- Custos inexistentes na fonte foram tratados como hipóteses documentadas.
- Modelos demonstrativos precisam de validação temporal antes de produção.
- Scores de RH, crédito, fraude e saúde não devem gerar decisões automáticas sobre pessoas.
- Correlação observacional não demonstra causalidade.

