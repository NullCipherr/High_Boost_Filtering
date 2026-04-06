# Handoff Técnico

## Estado atual

O projeto está estruturado para uso local e produção simples com Streamlit + Docker.

Funcionalidades entregues:

- processamento por CLI;
- interface web para upload/processamento/download;
- persistência opcional da saída em `Output_Images/`;
- validação automatizada com testes e lint;
- CI de qualidade no GitHub Actions.

## Pontos de operação

- Entrada padrão do pipeline CLI: `Input_Images/`.
- Saída padrão: `Output_Images/`.
- Porta da aplicação Streamlit: `8501`.

## Comandos essenciais

```bash
make install-dev
make lint
make test
make run-streamlit
make docker-run
```

## Contratos importantes

- `kernel_size` deve ser ímpar e >= 3.
- `sigma` deve ser > 0.
- Imagem é processada em escala de cinza.

## Próximos incrementos recomendados

1. Adicionar processamento em lote no Streamlit.
2. Incluir testes de integração para fluxo de upload/download.
3. Adicionar versionamento semântico e changelog.
