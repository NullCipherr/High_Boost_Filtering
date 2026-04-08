# Roadmap

## Visao do produto

Objetivo: evoluir de um filtro unico para uma suite de restauracao inteligente, capaz de melhorar imagens degradadas e, em cenarios especificos, reconstruir detalhes com IA.

Posicionamento:
- ferramenta tecnica para restauracao semicautomatica;
- foco em previsibilidade, transparencia de metricas e controle de risco;
- pronta para demos, portfolio e validacao comercial.

## Escopo funcional da V2

1. Diagnostico automatico de qualidade
- detectar nitidez, ruido, contraste, faixa dinamica e saturacao.
- gerar score agregado e recomendacao de estrategia.

2. Pipeline de restauracao classica adaptativa
- denoise condicional (quando ruido alto).
- high boost adaptativo por tipo de degradacao.
- equalizacao local opcional para recuperar contraste.

3. Pipeline de IA (opt-in)
- super-resolucao para baixa resolucao.
- restauracao facial quando houver rosto detectado.
- fluxo com fallback para metodo classico se IA falhar.

4. Comparacao de qualidade antes/depois
- score tecnico na interface.
- visualizacao lado a lado.
- historico simples das execucoes.

## Arquitetura alvo

Camadas propostas:
- `quality/`: diagnostico, score e recomendacoes.
- `classical/`: algoritmos tradicionais de restauracao.
- `ai/`: wrappers de modelos (via providers locais ou API).
- `orchestrator/`: motor de decisao e execucao do pipeline.
- `ui/`: Streamlit para operacao e comparacao.

## Politica de confiabilidade

- Nao prometer recuperacao fiel em 100 porcento dos casos.
- Marcar claramente quando o resultado foi inferido por IA.
- Permitir sempre baixar versao conservadora e versao agressiva.

## Backlog por fase

### Fase 1 - Diagnostico e decisao (curto prazo)
- [x] Modulo de diagnostico com score e recomendacao.
- [x] Exibicao de metricas no Streamlit.
- [ ] Persistencia do diagnostico em JSON por processamento.

### Fase 2 - Restauracao classica adaptativa
- [x] Denoise NLMeans com gatilho por perfil.
- [x] Modo auto do pipeline classico com presets.
- [ ] Benchmark interno com conjunto de imagens de referencia.

### Fase 3 - Produto e operacao
- [ ] Historico de jobs e reproducao de parametros.
- [ ] Relatorio exportavel antes/depois.
- [ ] Pagina de demonstracao e guia comercial.

## KPI do case

- melhoria media do score geral por categoria de degradacao;
- taxa de sucesso visual aprovada por avaliacao humana;
- tempo medio de processamento por imagem;
- custo por imagem em modo IA.

## Riscos e mitigacao

- Risco: superprocessamento com artefatos.
- Mitigacao: modo conservador padrao + limites por parametro.

- Risco: IA inventar detalhes inconsistentes.
- Mitigacao: aviso de inferencia e comparacao transparente lado a lado.

- Risco: latencia alta em hardware simples.
- Mitigacao: fallback classico e execucao por perfil de qualidade.
