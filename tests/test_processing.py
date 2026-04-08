import cv2
import numpy as np
import pytest

from high_boost_filtering.processing import (
    adaptive_classic_restore,
    apply_low_pass_filter,
    high_boost_filter,
)


def test_apply_low_pass_filter_preserva_shape():
    image = np.random.randint(0, 255, size=(64, 64), dtype=np.uint8)
    result = apply_low_pass_filter(image=image, kernel_size=5, sigma=1.0)

    assert result.shape == image.shape
    assert result.dtype == image.dtype


def test_high_boost_filter_preserva_limites_uint8():
    image = np.full((32, 32), 128, dtype=np.uint8)
    result = high_boost_filter(image=image, sharpening_factor=4.0, kernel_size=5, sigma=1.0)

    assert result.shape == image.shape
    assert result.min() >= 0
    assert result.max() <= 255


@pytest.mark.parametrize("kernel_size", [0, 2, 4])
def test_apply_low_pass_filter_rejeita_kernel_invalido(kernel_size: int):
    image = np.random.randint(0, 255, size=(32, 32), dtype=np.uint8)

    with pytest.raises(ValueError):
        apply_low_pass_filter(image=image, kernel_size=kernel_size, sigma=1.0)


def test_adaptive_classic_restore_preserva_formato():
    image = np.random.randint(0, 255, size=(64, 64), dtype=np.uint8)

    result = adaptive_classic_restore(image=image, profile_name="equilibrada")

    assert result.shape == image.shape
    assert result.dtype == image.dtype


def test_adaptive_classic_restore_rejeita_perfil_invalido():
    image = np.random.randint(0, 255, size=(64, 64), dtype=np.uint8)

    with pytest.raises(ValueError):
        adaptive_classic_restore(image=image, profile_name="nao-existe")


def test_adaptive_classic_restore_preserva_mais_bordas_quando_habilitado():
    image = np.full((128, 128), 90, dtype=np.uint8)
    image[:, 64:] = 220

    out_no_edges = adaptive_classic_restore(
        image=image,
        profile_name="denoise-primeiro",
        preserve_edges_enabled=False,
    )
    out_with_edges = adaptive_classic_restore(
        image=image,
        profile_name="denoise-primeiro",
        preserve_edges_enabled=True,
    )

    edge_mask = cv2.Canny(image, 50, 140) > 0
    diff_no_edges = np.abs(out_no_edges.astype(np.int16) - image.astype(np.int16))
    diff_with_edges = np.abs(out_with_edges.astype(np.int16) - image.astype(np.int16))

    assert diff_with_edges[edge_mask].mean() <= diff_no_edges[edge_mask].mean()
