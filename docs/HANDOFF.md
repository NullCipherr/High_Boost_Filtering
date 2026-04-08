# Handoff Tecnico

## Estado atual

Projeto estruturado com Streamlit + Docker + CI, agora evoluindo para suite de restauracao inteligente.

Funcionalidades ativas:

- processamento classico por high boost;
- modo auto adaptativo com presets classicos (denoise + high boost + clahe opcional);
- preservacao de bordas no modo auto para reduzir efeito borrado;
- diagnostico automatico de qualidade (score + recomendacao);
- comparativo antes/depois na interface;
- blend interativo antes/depois e mapa de diferenca com heatmap;
- export de relatorio tecnico em JSON;
- persistencia opcional em `Output_Images/`;
- validacao automatizada com testes e lint.

## Pontos de operacao

- Entrada padrao do pipeline CLI: `Input_Images/`.
- Saida padrao: `Output_Images/`.
- Porta da aplicacao Streamlit: `8501`.

## Comandos essenciais

```bash
make install-dev
make lint
make test
make run-streamlit
make docker-run
```

## Contratos tecnicos importantes

- `kernel_size` deve ser impar e >= 3.
- `sigma` deve ser > 0 (ou auto quando habilitado na UI).
- Diagnostico atual assume imagem em escala de cinza.

## Evolucao em andamento

- Roadmap estrategico: `docs/ROADMAP.md`.
- Proximo incremento recomendado: persistir relatorio de qualidade por execucao para analise historica.
