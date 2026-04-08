# Arquitetura Técnica

## Objetivo

Documentar a arquitetura atual do projeto para facilitar onboarding, manutenção e evolução da suíte de restauração.

## Visão em Camadas

### Entrypoints

- `main.py`: entrada da CLI para execução do pipeline por arquivo.
- `app_streamlit.py`: entrada da interface web (Streamlit).

### Núcleo de aplicação (`src/high_boost_filtering/`)

- `config.py`: parâmetros padrão e diretórios de entrada/saída.
- `cli.py`: parsing de argumentos e acionamento da pipeline em modo script.
- `pipeline.py`: orquestra leitura, processamento e persistência no fluxo CLI.
- `io_utils.py`: leitura e escrita de imagens em escala de cinza.
- `processing.py`: algoritmos de restauração clássica e presets adaptativos.
- `quality.py`: cálculo de métricas e recomendação de estratégia.
- `streamlit_app.py`: camada de apresentação e interação com usuário.

## Fluxos Principais

### Fluxo CLI

1. `cli.py` recebe argumentos (`--image`, `--k`, `--kernel-size`, `--sigma`).
2. `pipeline.py` resolve caminhos de entrada/saída.
3. `io_utils.py` carrega imagem em grayscale.
4. `processing.high_boost_filter()` aplica o filtro.
5. `io_utils.py` persiste resultado em `Output_Images/`.

### Fluxo Streamlit

1. Upload de imagem na UI.
2. `processing.decode_uploaded_image()` converte bytes para grayscale.
3. `quality.assess_image_quality()` calcula diagnóstico inicial.
4. Processamento:
   - manual: `high_boost_filter()`;
   - automático: `adaptive_classic_restore()` com preset recomendado.
5. Diagnóstico final + comparação visual + export de artefatos.

## Contratos Técnicos

- `kernel_size`: inteiro ímpar e maior ou igual a 3.
- `sigma`: float maior que 0 (quando manual).
- Escopo atual de imagem: tons de cinza (`uint8`).
- Perfis válidos do modo automático:
  - `conservadora`
  - `equilibrada`
  - `agressiva`
  - `denoise-primeiro`

## Decisões de Engenharia

- Separação forte entre processamento e UI.
- Diagnóstico de qualidade independente para permitir evolução do motor de decisão.
- Entrypoints simples na raiz para reduzir atrito de execução.
- Persistência em arquivos locais para facilitar operação offline e demos.

## Pontos de Evolução Recomendados

- Extrair estratégia de seleção de perfil para um orquestrador dedicado;
- Incluir histórico versionado de execuções (parâmetros + métricas);
- Evoluir para pipelines coloridos (RGB) sem quebrar o fluxo grayscale atual.
