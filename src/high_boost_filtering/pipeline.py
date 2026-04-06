from __future__ import annotations

from pathlib import Path

from .config import AppConfig
from .io_utils import load_grayscale_image, save_grayscale_image
from .processing import high_boost_filter


def process_image_file(
    image_filename: str,
    sharpening_factor: float,
    kernel_size: int,
    sigma: float,
    config: AppConfig,
) -> Path:
    """Processa uma imagem do diretório de entrada e salva no diretório de saída."""
    input_path = config.input_dir / image_filename
    image_name = Path(image_filename).stem
    output_path = config.output_dir / f"{image_name}_Sharpened.jpg"

    loaded_image = load_grayscale_image(input_path)
    sharpened_image = high_boost_filter(
        image=loaded_image,
        sharpening_factor=sharpening_factor,
        kernel_size=kernel_size,
        sigma=sigma,
    )
    return save_grayscale_image(sharpened_image, output_path)
