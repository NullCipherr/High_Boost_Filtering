from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from .config import DEFAULT_CONFIG
from .io_utils import save_grayscale_image
from .processing import (
    adaptive_classic_restore,
    decode_uploaded_image,
    encode_jpeg,
    high_boost_filter,
    sigma_from_kernel_size,
)
from .quality import assess_image_quality


def _build_diff_heatmap(original: np.ndarray, processed: np.ndarray) -> np.ndarray:
    diff = cv2.absdiff(processed, original)
    return cv2.applyColorMap(diff, cv2.COLORMAP_TURBO)


def run_streamlit_app() -> None:
    st.set_page_config(
        page_title="High Boost Filtering",
        page_icon="Imagem",
        layout="wide",
    )

    st.title("High Boost Filtering")
    st.caption("Aplique restauracao classica com modo manual e auto adaptativo.")

    with st.sidebar:
        st.header("Parametros")
        mode = st.radio(
            "Modo de processamento",
            options=["Manual", "Auto adaptativo"],
            index=1,
            help="Auto adaptativo usa diagnostico para escolher preset classico.",
        )

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
            help="No modo manual, recalcula sigma conforme o kernel.",
        )

        if auto_sigma:
            sigma = sigma_from_kernel_size(kernel_size)
            st.caption(f"Sigma automatico atual: {sigma:.2f}")
        else:
            sigma = st.slider("Sigma", 0.1, 10.0, DEFAULT_CONFIG.default_sigma, 0.1)

        auto_strength = st.slider(
            "Intensidade do auto adaptativo",
            0.6,
            1.4,
            1.0,
            0.05,
            help="Controla forca dos presets no modo automatico.",
        )
        preserve_edges_enabled = st.checkbox(
            "Preservar bordas no modo automatico",
            value=True,
            help="Reduz aspecto borrado mesclando informacao de bordas da imagem original.",
        )

    uploaded_file = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])

    if uploaded_file is None:
        st.info("Faça upload de uma imagem para iniciar.")
        return

    original_image = decode_uploaded_image(uploaded_file.read())
    if original_image is None:
        st.error("Falha ao ler o arquivo enviado.")
        return

    original_report = assess_image_quality(original_image)

    if mode == "Auto adaptativo":
        selected_profile = original_report.recommendation
        processed_image = adaptive_classic_restore(
            image=original_image,
            profile_name=selected_profile,
            strength=auto_strength,
            preserve_edges_enabled=preserve_edges_enabled,
        )
    else:
        selected_profile = "manual"
        processed_image = high_boost_filter(
            image=original_image,
            sharpening_factor=sharpening_factor,
            kernel_size=kernel_size,
            sigma=sigma,
        )

    processed_report = assess_image_quality(processed_image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, clamp=True, width="stretch")
    with col2:
        st.subheader("Processada")
        st.image(processed_image, clamp=True, width="stretch")

    st.subheader("Diagnostico de Qualidade")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            "Score Geral",
            f"{processed_report.overall_score:.1f}",
            f"{processed_report.overall_score - original_report.overall_score:+.1f}",
        )
    with m2:
        st.metric(
            "Nitidez (Laplaciano)",
            f"{processed_report.sharpness_score:.1f}",
            f"{processed_report.sharpness_score - original_report.sharpness_score:+.1f}",
        )
    with m3:
        st.metric(
            "Ruido Estimado",
            f"{processed_report.noise_score:.2f}",
            f"{processed_report.noise_score - original_report.noise_score:+.2f}",
        )

    if processed_report.sharpness_score < (original_report.sharpness_score * 0.85):
        st.warning(
            "A nitidez caiu em relacao a imagem original. "
            "Tente reduzir a intensidade do auto adaptativo."
        )

    st.caption(
        "Recomendacao automatica para pipeline avancado: "
        f"{processed_report.recommendation} | Perfil aplicado: {selected_profile}"
    )

    # Funcionalidade 1: blend interativo antes/depois.
    st.subheader("Comparacao Avancada")
    blend_percent = st.slider("Mistura Antes/Depois (%)", 0, 100, 50, 5)
    blend_alpha = blend_percent / 100.0
    blend_image = cv2.addWeighted(
        original_image,
        1.0 - blend_alpha,
        processed_image,
        blend_alpha,
        0,
    )
    st.image(
        blend_image,
        clamp=True,
        width="stretch",
        caption=f"Blend com {blend_percent}% da imagem processada",
    )

    # Funcionalidade 2: mapa de diferenca + heatmap.
    with st.expander("Mapa de diferenca e heatmap"):
        diff_map = cv2.absdiff(processed_image, original_image)
        heatmap = _build_diff_heatmap(original_image, processed_image)
        d1, d2 = st.columns(2)
        with d1:
            st.image(diff_map, clamp=True, width="stretch", caption="Diferenca absoluta")
        with d2:
            st.image(
                cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB),
                width="stretch",
                caption="Heatmap de alteracoes",
            )

    base_name = Path(uploaded_file.name).stem

    st.download_button(
        label="Baixar imagem processada",
        data=encode_jpeg(processed_image),
        file_name=f"{base_name}_Sharpened.jpg",
        mime="image/jpeg",
    )

    # Funcionalidade 3: export de relatorio tecnico JSON.
    report_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "selected_profile": selected_profile,
        "params": {
            "manual": {
                "sharpening_factor": sharpening_factor,
                "kernel_size": kernel_size,
                "sigma": sigma,
                "auto_sigma": auto_sigma,
            },
            "auto": {
                "strength": auto_strength,
                "preserve_edges_enabled": preserve_edges_enabled,
            },
        },
        "original_report": asdict(original_report),
        "processed_report": asdict(processed_report),
    }
    st.download_button(
        label="Baixar relatorio tecnico (JSON)",
        data=json.dumps(report_payload, indent=2, ensure_ascii=False),
        file_name=f"{base_name}_report.json",
        mime="application/json",
    )

    if st.button("Salvar tambem em Output_Images"):
        output_path = DEFAULT_CONFIG.output_dir / f"{base_name}_Sharpened.jpg"
        saved_path = save_grayscale_image(processed_image, output_path)
        st.success(f"Imagem salva em: {saved_path}")
