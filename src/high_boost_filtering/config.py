from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Configuração central do projeto."""

    input_dir: Path = Path("Input_Images")
    output_dir: Path = Path("Output_Images")
    default_image_filename: str = "Image_004.jpg"
    default_sharpening_factor: float = 4.0
    default_kernel_size: int = 5
    default_sigma: float = 1.0


DEFAULT_CONFIG = AppConfig()
