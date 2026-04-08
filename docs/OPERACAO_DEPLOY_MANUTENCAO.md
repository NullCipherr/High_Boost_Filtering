# Operação, Deploy e Manutenção

## Requisitos

- Python 3.10+
- pip
- Docker e Docker Compose (opcional)

## Setup Local

Instalação de dependências de desenvolvimento:

```bash
make install-dev
```

Alternativa:

```bash
pip install -r requirements-dev.txt
```

## Execução

### CLI

```bash
python main.py --image Image_004.jpg --k 4.0 --kernel-size 5 --sigma 1.0
```

Entrada esperada: `Input_Images/`.
Saída gerada: `Output_Images/<nome>_Sharpened.jpg`.

### Streamlit

```bash
streamlit run app_streamlit.py
```

Acesso local: `http://localhost:8501`.

## Operação com Docker

Build da imagem:

```bash
docker build -t high-boost-filtering:latest .
```

Subida da aplicação:

```bash
docker compose up --build
```

Volumes relevantes:

- `./Input_Images -> /app/Input_Images`
- `./Output_Images -> /app/Output_Images`

## Comandos de Rotina (Make)

- `make run`: executa CLI com configuração padrão.
- `make run-streamlit`: inicia a interface web.
- `make lint`: valida estilo e problemas estáticos.
- `make test`: executa suíte de testes.
- `make docker-build`: build de container.
- `make docker-run`: sobe stack local com compose.

## Estratégia de Manutenção

### Atualização de dependências

1. Atualizar `requirements.txt` e/ou `requirements-dev.txt`.
2. Rodar `make lint` e `make test`.
3. Validar execução manual da UI e da CLI.

### Checklist antes de release

1. Lint e testes passando localmente.
2. Processamento validado com imagem real em `Input_Images/`.
3. Fluxo Streamlit validado (upload, processamento, download, JSON).
4. README e docs sincronizados com comportamento atual.

### Troubleshooting rápido

- Erro ao carregar imagem: confirmar arquivo em `Input_Images/` e nome correto.
- Resultado inesperado no auto adaptativo: reduzir intensidade (`auto_strength`) e manter preservação de bordas habilitada.
- Falha em container: verificar porta `8501` livre e logs do serviço no Docker.
