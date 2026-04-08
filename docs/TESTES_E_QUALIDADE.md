# Testes e Qualidade

## Objetivo

Definir o padrão mínimo de qualidade para manter previsibilidade no processamento e estabilidade na evolução do projeto.

## Ferramentas

- `pytest`: testes unitários
- `ruff`: lint estático
- GitHub Actions: execução automática no CI

## Execução Local

### Lint

```bash
make lint
```

### Testes

```bash
make test
```

## Cobertura Atual de Testes

### `tests/test_processing.py`

- preservação de `shape` e `dtype` no filtro passa-baixa;
- validação de limites em saída `uint8` no high boost;
- rejeição de `kernel_size` inválido;
- contrato de perfil válido/inválido no auto adaptativo;
- verificação de preservação de bordas quando habilitada.

### `tests/test_quality.py`

- faixa válida do score geral (`0-100`);
- recomendação dentro dos perfis suportados;
- sensibilidade de nitidez com imagem de bordas;
- detecção de diferença de contraste.

## CI

Pipeline em `.github/workflows/ci.yml` com etapas:

1. Setup Python 3.11;
2. Instalação de `requirements-dev.txt`;
3. `ruff check src tests`;
4. `pytest -q`.

## Critério de Aceite para PR

1. Sem regressão funcional em CLI/Streamlit.
2. Lint e testes locais aprovados.
3. Evidência de validação do fluxo alterado.
4. Documentação atualizada quando houver mudança de contrato.

## Gaps Conhecidos

- Ainda não há testes de integração ponta-a-ponta da interface Streamlit.
- Não existe benchmark automatizado com dataset de referência versionado.
- Não há teste de regressão visual com baseline de imagens.

## Próximos Incrementos Recomendados

1. Adicionar teste de integração do fluxo CLI com arquivos temporários.
2. Criar suíte de regressão visual com thresholds de diferença.
3. Automatizar coleta de métricas de qualidade por execução em artefatos versionáveis.
