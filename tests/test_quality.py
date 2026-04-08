import numpy as np

from high_boost_filtering.quality import (
    assess_image_quality,
    estimate_contrast,
    estimate_sharpness_laplacian,
)


def test_assess_image_quality_retorna_faixa_valida():
    image = np.random.randint(0, 255, size=(128, 128), dtype=np.uint8)
    report = assess_image_quality(image)

    assert 0.0 <= report.overall_score <= 100.0
    assert report.recommendation in {
        "agressiva",
        "equilibrada",
        "denoise-primeiro",
        "conservadora",
    }


def test_sharpness_maior_em_imagem_com_bordas():
    soft = np.full((128, 128), 128, dtype=np.uint8)
    sharp = soft.copy()
    sharp[:, 64:] = 255

    soft_score = estimate_sharpness_laplacian(soft)
    sharp_score = estimate_sharpness_laplacian(sharp)

    assert sharp_score > soft_score


def test_contrast_detecta_diferenca_de_faixa():
    low_contrast = np.full((128, 128), 110, dtype=np.uint8)
    high_contrast = np.vstack(
        [
            np.full((64, 128), 20, dtype=np.uint8),
            np.full((64, 128), 230, dtype=np.uint8),
        ]
    )

    assert estimate_contrast(high_contrast) > estimate_contrast(low_contrast)
