<div align="center">
  <h1>High Boost Filtering</h1>
  <p><i>Suite de restauração de imagem em escala de cinza com High Boost Filtering, diagnóstico de qualidade e operação via CLI + Streamlit</i></p>

  <p>
    <a href=".github/workflows/ci.yml"><img src="https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="CI" /></a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV" />
    <img src="https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  </p>
</div>

---

## Documentação

A documentação técnica e operacional está organizada em `docs/`:

- [Índice da Documentação](docs/README.md)
- [Arquitetura Técnica](docs/ARQUITETURA.md)
- [Operação, Deploy e Manutenção](docs/OPERACAO_DEPLOY_MANUTENCAO.md)
- [Testes e Qualidade](docs/TESTES_E_QUALIDADE.md)
- [Handoff Técnico](docs/HANDOFF.md)
- [Roadmap](docs/ROADMAP.md)
- [Guia de Contribuição](CONTRIBUTING.md)

---

## Visão Geral

O **High Boost Filtering** evolui de um filtro clássico para uma base de suite de restauração com foco em:

- previsibilidade dos resultados;
- separação clara entre processamento, IO e interface;
- diagnóstico automatizado de qualidade;
- execução local e containerizada para operação consistente.

Atualmente, o projeto trabalha com **imagens em escala de cinza**.

---

## Funcionalidades

- **Pipeline clássico (CLI)** para processamento de imagens em lote manual por parâmetros.
- **Interface Streamlit** para operação visual com upload de imagem.
- **Modo Manual** com controle de `k`, `kernel_size` e `sigma`.
- **Modo Auto adaptativo** com presets:
  - `conservadora`
  - `equilibrada`
  - `agressiva`
  - `denoise-primeiro`
- **Diagnóstico técnico de qualidade** (antes/depois):
  - score geral;
  - nitidez (variância do Laplaciano);
  - ruído estimado;
  - contraste e faixa dinâmica;
  - saturação em extremos escuro/claro.
- **Preservação de bordas** no modo automático para reduzir borramento.
- **Comparação avançada** na UI:
  - blend antes/depois;
  - mapa de diferença absoluta;
  - heatmap de alterações.
- **Exportações**:
  - imagem processada (`.jpg`);
  - relatório técnico (`.json`) com parâmetros e métricas.
- **Qualidade de código** com `pytest`, `ruff` e CI no GitHub Actions.

---

## Arquitetura

Fluxo principal:

1. Entrada via CLI (`main.py`) ou app web (`app_streamlit.py`).
2. Leitura/decodificação da imagem em escala de cinza.
3. Diagnóstico de qualidade inicial para recomendação de perfil.
4. Processamento por High Boost (manual) ou pipeline clássico adaptativo (auto).
5. Diagnóstico pós-processamento, comparação visual e exportação de artefatos.

Decisão de camadas:

- `processing.py`: algoritmos (filtro passa-baixa, high boost, denoise, CLAHE, preservação de bordas).
- `quality.py`: métricas e recomendação de estratégia.
- `io_utils.py`: leitura e persistência de imagens.
- `pipeline.py`: orquestração do fluxo de arquivo (CLI).
- `streamlit_app.py`: experiência interativa e relatórios de execução.
- `config.py`: configuração central do projeto.

---

## Stack Técnica

- **Linguagem**: Python 3.10+
- **Processamento de imagem**: OpenCV + NumPy
- **Interface web**: Streamlit
- **Testes**: Pytest
- **Lint**: Ruff
- **Containerização**: Docker + Docker Compose
- **Automação local**: Makefile

---

## Estrutura do Projeto

```text
.
├── .github/workflows/ci.yml
├── .streamlit/config.toml
├── docs/
│   ├── README.md
│   ├── ARQUITETURA.md
│   ├── HANDOFF.md
│   ├── OPERACAO_DEPLOY_MANUTENCAO.md
│   ├── ROADMAP.md
│   └── TESTES_E_QUALIDADE.md
├── src/high_boost_filtering/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── io_utils.py
│   ├── pipeline.py
│   ├── processing.py
│   ├── quality.py
│   └── streamlit_app.py
├── tests/
│   ├── test_processing.py
│   └── test_quality.py
├── Input_Images/
├── Output_Images/
├── app_streamlit.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── CONTRIBUTING.md
└── README.md
```

---

## Começando Rápido

### Pré-requisitos

- Python `3.10+`
- `pip`
- Docker + Docker Compose (opcional)

### Instalação

Com Make:

```bash
make install-dev
```

Ou manualmente:

```bash
pip install -r requirements-dev.txt
```

---

## Execução Local

### CLI

Processa uma imagem de `Input_Images/` e salva em `Output_Images/`.

```bash
python main.py --image Image_004.jpg --k 4.0 --kernel-size 5 --sigma 1.0
```

Parâmetros disponíveis:

- `--image`: nome do arquivo dentro de `Input_Images`
- `--k`: fator de nitidez
- `--kernel-size`: tamanho do kernel (ímpar e `>= 3`)
- `--sigma`: sigma do Gaussiano (`> 0`)

### Streamlit

```bash
streamlit run app_streamlit.py
```

Acesso local: `http://localhost:8501`

---

## Docker

### Build da imagem

```bash
docker build -t high-boost-filtering:latest .
```

### Subir com Compose

```bash
docker compose up --build
```

Acesso local: `http://localhost:8501`

Volumes mapeados:

- `./Input_Images -> /app/Input_Images`
- `./Output_Images -> /app/Output_Images`

---

## Qualidade e CI

### Lint

```bash
make lint
```

### Testes

```bash
make test
```

### Pipeline de CI

Workflow: `.github/workflows/ci.yml`

Etapas:

1. Instala dependências de desenvolvimento.
2. Executa `ruff check src tests`.
3. Executa `pytest -q`.

---

## Targets do Makefile

- `make install`: instala dependências de runtime.
- `make install-dev`: instala dependências de desenvolvimento.
- `make run`: executa o pipeline CLI.
- `make run-streamlit`: inicia a interface Streamlit.
- `make test`: executa testes unitários.
- `make lint`: executa lint com Ruff.
- `make docker-build`: build da imagem Docker.
- `make docker-run`: sobe stack local via Docker Compose.

---

## Contratos Técnicos Importantes

- O pipeline assume **imagem em escala de cinza**.
- `kernel_size` deve ser **ímpar** e **maior ou igual a 3**.
- `sigma` deve ser **maior que 0** quando usado manualmente.
- No modo auto, o perfil é recomendado por diagnóstico da imagem de entrada.

---

## Roadmap

Direcionadores principais de evolução (detalhes em `docs/ROADMAP.md`):

- persistência de diagnósticos por execução;
- benchmark com conjunto de imagens de referência;
- histórico de jobs e reprodução de parâmetros;
- camada opcional de IA (opt-in) com fallback clássico.

---

## Contribuição

Contribuições são bem-vindas.

Antes de abrir PR:

1. Execute `make lint`.
2. Execute `make test`.
3. Documente impacto técnico e evidências da mudança.

Guia completo: [CONTRIBUTING.md](CONTRIBUTING.md)

<div align="center">
  Construído para evolução incremental, previsível e orientada por métricas de qualidade de imagem.
</div>
