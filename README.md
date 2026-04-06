# High Boost Filtering

Aplicação de processamento de imagem com **High Boost Filtering**, oferecendo:

- pipeline via script/CLI;
- interface web com Streamlit;
- execução containerizada com Docker;
- estrutura pronta para colaboração no GitHub (CI, testes, lint e documentação).

## Objetivo

Realçar detalhes de alta frequência (bordas e texturas) em imagens em escala de cinza, com controle de parâmetros para ajuste fino da nitidez.

## Arquitetura do projeto

```text
high-boost-filtering/
├── .github/workflows/ci.yml
├── .streamlit/config.toml
├── docs/
│   └── HANDOFF.md
├── src/
│   └── high_boost_filtering/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── io_utils.py
│       ├── pipeline.py
│       ├── processing.py
│       └── streamlit_app.py
├── tests/
│   └── test_processing.py
├── app_streamlit.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

## Decisões de design

- Separação de responsabilidades:
- `processing.py`: regras matemáticas dos filtros.
- `io_utils.py`: leitura/gravação de arquivos.
- `pipeline.py`: orquestra fluxo de entrada/processamento/saída.
- `streamlit_app.py`: camada de interface.
- Entrypoints na raiz para UX simples (`main.py` e `app_streamlit.py`).

## Requisitos

- Python 3.10+
- pip
- Docker (opcional, para execução em container)

## Setup local

```bash
make install-dev
```

Ou:

```bash
pip install -r requirements-dev.txt
```

## Executando localmente

### CLI (processa imagem de `Input_Images/`)

```bash
python main.py --image Image_004.jpg --k 4.0 --kernel-size 5 --sigma 1.0
```

### Streamlit

```bash
streamlit run app_streamlit.py
```

Acesse: `http://localhost:8501`

Observação de parâmetro:
- Na interface, o modo padrão usa **sigma automático por kernel** para que mudanças em `kernel_size` gerem efeito visual mais claro.
- Se preferir controle manual, desative a opção e ajuste `sigma` livremente.

## Docker

### Build da imagem

```bash
docker build -t high-boost-filtering:latest .
```

### Subir com Docker Compose

```bash
docker compose up --build
```

A interface estará em `http://localhost:8501`.

Volumes mapeados:

- `./Input_Images -> /app/Input_Images`
- `./Output_Images -> /app/Output_Images`

## Qualidade

### Lint

```bash
make lint
```

### Testes

```bash
make test
```

### CI

Pipeline GitHub Actions (`.github/workflows/ci.yml`) roda:

1. `ruff check src tests`
2. `pytest -q`

## Boas práticas de manutenção

- Não misturar UI com lógica matemática de processamento.
- Tratar novas integrações em camadas específicas.
- Priorizar mudanças pequenas e testáveis.
- Atualizar README e docs sempre que o fluxo de execução mudar.

## Roadmap sugerido

1. Suporte a processamento em lote via UI.
2. Exportação opcional em PNG/JPEG com qualidade configurável.
3. Métricas de qualidade de imagem (PSNR/SSIM) para comparação.
