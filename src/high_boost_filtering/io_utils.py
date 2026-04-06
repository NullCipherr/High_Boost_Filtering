from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def load_grayscale_image(image_path: Path) -> np.ndarray:
    """Carrega imagem em escala de cinza a partir do caminho informado."""
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem: {image_path}")
    return image


def save_grayscale_image(image: np.ndarray, output_path: Path) -> Path:
    """Salva imagem em escala de cinza no caminho de saída."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    return output_path
