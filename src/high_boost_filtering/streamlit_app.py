from __future__ import annotations

from pathlib import Path

import streamlit as st

from .config import DEFAULT_CONFIG
from .io_utils import save_grayscale_image
from .processing import (
    decode_uploaded_image,
    encode_jpeg,
    high_boost_filter,
    sigma_from_kernel_size,
)


def run_streamlit_app() -> None:
    st.set_page_config(
        page_title="High Boost Filtering",
        page_icon="Imagem",
        layout="wide",
    )

    st.title("High Boost Filtering")
    st.caption("Aplique nitidez em imagens em escala de cinza com parâmetros ajustáveis.")

    with st.sidebar:
        st.header("Parâmetros")
        sharpening_factor = st.slider(
            "Fator de nitidez (k)",
            0.0,
            10.0,
            DEFAULT_CONFIG.default_sharpening_factor,
            0.1,
        )
        kernel_size = st.slider(
            "Tamanho do kernel",
            3,
            31,
            DEFAULT_CONFIG.default_kernel_size,
            2,
        )
        auto_sigma = st.checkbox(
            "Ajustar sigma automaticamente pelo kernel",
            value=True,
            help=(
                "Quando ativo, o sigma é recalculado conforme o kernel "
                "para tornar o efeito mais perceptível."
            ),
        )
        if auto_sigma:
            sigma = sigma_from_kernel_size(kernel_size)
            st.caption(f"Sigma automático atual: {sigma:.2f}")
        else:
            sigma = st.slider("Sigma", 0.1, 10.0, DEFAULT_CONFIG.default_sigma, 0.1)

    uploaded_file = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])

    if uploaded_file is None:
        st.info("Faça upload de uma imagem para iniciar.")
        return

    original_image = decode_uploaded_image(uploaded_file.read())
    if original_image is None:
        st.error("Falha ao ler o arquivo enviado.")
        return

    processed_image = high_boost_filter(
        image=original_image,
        sharpening_factor=sharpening_factor,
        kernel_size=kernel_size,
        sigma=sigma,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, clamp=True, width="stretch")
    with col2:
        st.subheader("Processada")
        st.image(processed_image, clamp=True, width="stretch")

    base_name = Path(uploaded_file.name).stem
    st.download_button(
        label="Baixar imagem processada",
        data=encode_jpeg(processed_image),
        file_name=f"{base_name}_Sharpened.jpg",
        mime="image/jpeg",
    )

    if st.button("Salvar também em Output_Images"):
        output_path = DEFAULT_CONFIG.output_dir / f"{base_name}_Sharpened.jpg"
        saved_path = save_grayscale_image(processed_image, output_path)
        st.success(f"Imagem salva em: {saved_path}")
