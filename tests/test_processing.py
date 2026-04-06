import numpy as np
import pytest

from high_boost_filtering.processing import apply_low_pass_filter, high_boost_filter


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
