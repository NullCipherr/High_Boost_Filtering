# Contribuindo

## Fluxo recomendado

1. Abra uma issue descrevendo problema, contexto e resultado esperado.
2. Crie branch com prefixo claro, por exemplo: `feat/`, `fix/`, `chore/`.
3. Faça alterações pequenas e coesas.
4. Execute qualidade local antes do commit:

```bash
make lint
make test
```

5. Abra Pull Request com:
- resumo técnico;
- motivação da mudança;
- impacto esperado;
- evidências (prints/gifs para UI quando aplicável).

## Convenções

- Código e documentação em pt-BR.
- Nomes claros para módulos, funções e variáveis.
- Lógica de processamento isolada de camada de UI.
- Evitar dependências novas sem justificativa técnica.

## Revisão

PRs são avaliados por:
- legibilidade e manutenibilidade;
- cobertura de testes para comportamento crítico;
- impacto em performance e UX.
