from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class ImageQualityReport:
    """Relatório de qualidade para orientar o pipeline de restauração."""

    sharpness_score: float
    noise_score: float
    contrast_score: float
    dynamic_range_score: float
    saturation_dark_pct: float
    saturation_bright_pct: float
    overall_score: float
    recommendation: str


def _normalize(value: float, min_value: float, max_value: float) -> float:
    if max_value <= min_value:
        return 0.0
    bounded = max(min_value, min(max_value, value))
    return (bounded - min_value) / (max_value - min_value)


def estimate_sharpness_laplacian(image: np.ndarray) -> float:
    """Estima nitidez usando variância do Laplaciano (quanto maior, mais nítida)."""
    lap = cv2.Laplacian(image, cv2.CV_64F)
    return float(lap.var())


def estimate_noise(image: np.ndarray) -> float:
    """Estima ruído por energia de alta frequência após suavização leve."""
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    residual = image.astype(np.float32) - blurred.astype(np.float32)
    return float(np.std(residual))


def estimate_contrast(image: np.ndarray) -> float:
    """Contraste global pela diferença entre percentis 95 e 5."""
    p05, p95 = np.percentile(image, [5, 95])
    return float(p95 - p05)


def estimate_dynamic_range(image: np.ndarray) -> float:
    """Faixa dinâmica utilizando percentis robustos para reduzir outliers."""
    p01, p99 = np.percentile(image, [1, 99])
    return float(p99 - p01)


def estimate_saturation(image: np.ndarray) -> tuple[float, float]:
    """Percentual de pixels próximos dos extremos escuro e claro."""
    dark_pct = float(np.mean(image <= 5) * 100.0)
    bright_pct = float(np.mean(image >= 250) * 100.0)
    return dark_pct, bright_pct


def pick_recommendation(
    sharpness_score: float,
    noise_score: float,
    contrast_score: float,
) -> str:
    """Define perfil de restauração inicial."""
    if sharpness_score < 30 and noise_score < 12:
        return "agressiva"
    if sharpness_score < 70 or contrast_score < 40:
        return "equilibrada"
    if noise_score > 20:
        return "denoise-primeiro"
    return "conservadora"


def assess_image_quality(image: np.ndarray) -> ImageQualityReport:
    """Gera diagnóstico completo de qualidade da imagem em escala de cinza."""
    sharpness_score = estimate_sharpness_laplacian(image)
    noise_score = estimate_noise(image)
    contrast_score = estimate_contrast(image)
    dynamic_range_score = estimate_dynamic_range(image)
    saturation_dark_pct, saturation_bright_pct = estimate_saturation(image)

    # Escore agregado (0-100) para acompanhamento de evolução no pipeline.
    sharpness_norm = _normalize(sharpness_score, 10.0, 250.0)
    noise_norm = 1.0 - _normalize(noise_score, 3.0, 35.0)
    contrast_norm = _normalize(contrast_score, 20.0, 160.0)
    dynamic_norm = _normalize(dynamic_range_score, 20.0, 180.0)
    clipping_penalty = _normalize(saturation_dark_pct + saturation_bright_pct, 0.0, 50.0)

    overall_score = (
        (sharpness_norm * 0.35)
        + (noise_norm * 0.2)
        + (contrast_norm * 0.2)
        + (dynamic_norm * 0.2)
        + ((1.0 - clipping_penalty) * 0.05)
    ) * 100.0

    recommendation = pick_recommendation(
        sharpness_score=sharpness_score,
        noise_score=noise_score,
        contrast_score=contrast_score,
    )

    return ImageQualityReport(
        sharpness_score=sharpness_score,
        noise_score=noise_score,
        contrast_score=contrast_score,
        dynamic_range_score=dynamic_range_score,
        saturation_dark_pct=saturation_dark_pct,
        saturation_bright_pct=saturation_bright_pct,
        overall_score=overall_score,
        recommendation=recommendation,
    )
