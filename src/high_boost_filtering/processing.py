from __future__ import annotations

import cv2
import numpy as np


def sigma_from_kernel_size(kernel_size: int) -> float:
    """Calcula um sigma proporcional ao kernel (aproximação comum do OpenCV)."""
    if kernel_size < 3 or kernel_size % 2 == 0:
        raise ValueError("kernel_size deve ser ímpar e maior ou igual a 3.")
    return 0.3 * (((kernel_size - 1) * 0.5) - 1) + 0.8


def decode_uploaded_image(file_bytes: bytes) -> np.ndarray | None:
    """Decodifica bytes de upload para imagem em escala de cinza."""
    np_buffer = np.frombuffer(file_bytes, dtype=np.uint8)
    return cv2.imdecode(np_buffer, cv2.IMREAD_GRAYSCALE)


def apply_low_pass_filter(image: np.ndarray, kernel_size: int, sigma: float) -> np.ndarray:
    """Aplica filtro gaussiano passa-baixa com kernel construído manualmente."""
    if kernel_size < 3 or kernel_size % 2 == 0:
        raise ValueError("kernel_size deve ser ímpar e maior ou igual a 3.")
    if sigma <= 0:
        raise ValueError("sigma deve ser maior que 0.")

    offset = kernel_size // 2
    x = np.arange(-offset, offset + 1).reshape(1, -1)
    y = np.arange(-offset, offset + 1).reshape(-1, 1)

    kernel = np.exp(-((x**2 + y**2) / (2 * sigma**2)))
    kernel /= np.sum(kernel)

    return cv2.filter2D(image, -1, kernel)


def high_boost_filter(
    image: np.ndarray,
    sharpening_factor: float,
    kernel_size: int,
    sigma: float,
) -> np.ndarray:
    """Executa high-boost filtering em imagem de tons de cinza."""
    filtered_image = apply_low_pass_filter(image=image, kernel_size=kernel_size, sigma=sigma)
    return cv2.addWeighted(image, 1 + sharpening_factor, filtered_image, -sharpening_factor, 0)


def encode_jpeg(image: np.ndarray) -> bytes:
    """Codifica a imagem em JPEG para download."""
    success, encoded = cv2.imencode(".jpg", image)
    if not success:
        raise RuntimeError("Falha ao codificar imagem em JPEG.")
    return encoded.tobytes()
