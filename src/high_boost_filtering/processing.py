from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class ClassicProfile:
    """Preset do pipeline classico adaptativo."""

    denoise_method: str
    denoise_strength: float
    sharpening_factor: float
    kernel_size: int
    use_auto_sigma: bool
    sigma: float
    use_clahe: bool
    clahe_clip_limit: float
    clahe_tile_grid_size: int
    detail_recovery_amount: float


PROFILES: dict[str, ClassicProfile] = {
    "conservadora": ClassicProfile(
        denoise_method="none",
        denoise_strength=0.0,
        sharpening_factor=1.8,
        kernel_size=5,
        use_auto_sigma=True,
        sigma=1.0,
        use_clahe=False,
        clahe_clip_limit=2.0,
        clahe_tile_grid_size=8,
        detail_recovery_amount=0.10,
    ),
    "equilibrada": ClassicProfile(
        denoise_method="bilateral",
        denoise_strength=0.9,
        sharpening_factor=2.8,
        kernel_size=5,
        use_auto_sigma=True,
        sigma=1.0,
        use_clahe=True,
        clahe_clip_limit=1.8,
        clahe_tile_grid_size=8,
        detail_recovery_amount=0.15,
    ),
    "agressiva": ClassicProfile(
        denoise_method="nlmeans",
        denoise_strength=9.0,
        sharpening_factor=3.8,
        kernel_size=7,
        use_auto_sigma=True,
        sigma=1.2,
        use_clahe=True,
        clahe_clip_limit=2.1,
        clahe_tile_grid_size=8,
        detail_recovery_amount=0.20,
    ),
    "denoise-primeiro": ClassicProfile(
        denoise_method="nlmeans",
        denoise_strength=10.0,
        sharpening_factor=2.4,
        kernel_size=5,
        use_auto_sigma=True,
        sigma=1.0,
        use_clahe=False,
        clahe_clip_limit=2.0,
        clahe_tile_grid_size=8,
        detail_recovery_amount=0.25,
    ),
}


def sigma_from_kernel_size(kernel_size: int) -> float:
    """Calcula um sigma proporcional ao kernel (aproximacao comum do OpenCV)."""
    if kernel_size < 3 or kernel_size % 2 == 0:
        raise ValueError("kernel_size deve ser impar e maior ou igual a 3.")
    return 0.3 * (((kernel_size - 1) * 0.5) - 1) + 0.8


def decode_uploaded_image(file_bytes: bytes) -> np.ndarray | None:
    """Decodifica bytes de upload para imagem em escala de cinza."""
    np_buffer = np.frombuffer(file_bytes, dtype=np.uint8)
    return cv2.imdecode(np_buffer, cv2.IMREAD_GRAYSCALE)


def apply_low_pass_filter(image: np.ndarray, kernel_size: int, sigma: float) -> np.ndarray:
    """Aplica filtro gaussiano passa-baixa com kernel construido manualmente."""
    if kernel_size < 3 or kernel_size % 2 == 0:
        raise ValueError("kernel_size deve ser impar e maior ou igual a 3.")
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


def apply_denoise_nlmeans(image: np.ndarray, h: float = 10.0) -> np.ndarray:
    """Denoise nao-local com melhor preservacao de contornos."""
    return cv2.fastNlMeansDenoising(image, None, h=h, templateWindowSize=7, searchWindowSize=21)


def apply_denoise_bilateral(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """Denoise bilateral leve para reduzir ruido sem borrar bordas."""
    sigma_color = 45.0 * max(0.3, strength)
    sigma_space = 45.0 * max(0.3, strength)
    return cv2.bilateralFilter(image, d=7, sigmaColor=sigma_color, sigmaSpace=sigma_space)


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: int = 8,
) -> np.ndarray:
    """Aplica CLAHE para recuperar contraste local sem estourar tons."""
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_grid_size, tile_grid_size),
    )
    return clahe.apply(image)


def recover_details_unsharp(
    reference_image: np.ndarray,
    target_image: np.ndarray,
    amount: float,
) -> np.ndarray:
    """Recupera detalhes finos usando mascara unsharp derivada da imagem original."""
    blurred_ref = cv2.GaussianBlur(reference_image, (0, 0), 1.2)
    detail = cv2.subtract(reference_image, blurred_ref)
    recovered = cv2.addWeighted(target_image, 1.0, detail, amount, 0)
    return np.clip(recovered, 0, 255).astype(np.uint8)


def preserve_edges(
    original_image: np.ndarray,
    processed_image: np.ndarray,
    strength: float,
) -> np.ndarray:
    """Mescla bordas originais para evitar aspecto borrado no modo automatico."""
    edge_map = cv2.Canny(original_image, 50, 140)
    edge_mask = cv2.GaussianBlur(edge_map.astype(np.float32) / 255.0, (7, 7), 0)
    edge_mask = np.clip(edge_mask * strength, 0.0, 1.0)

    out = (
        processed_image.astype(np.float32) * (1.0 - edge_mask)
        + original_image.astype(np.float32) * edge_mask
    )
    return np.clip(out, 0, 255).astype(np.uint8)


def get_profile(profile_name: str) -> ClassicProfile:
    """Retorna preset por nome para pipeline classico adaptativo."""
    if profile_name not in PROFILES:
        raise ValueError(
            f"Perfil desconhecido: {profile_name}. "
            f"Perfis validos: {', '.join(PROFILES.keys())}."
        )
    return PROFILES[profile_name]


def adaptive_classic_restore(
    image: np.ndarray,
    profile_name: str,
    strength: float = 1.0,
    preserve_edges_enabled: bool = True,
) -> np.ndarray:
    """Executa pipeline classico adaptativo conforme o perfil recomendado."""
    profile = get_profile(profile_name)
    output = image.copy()

    if profile.denoise_method == "nlmeans":
        output = apply_denoise_nlmeans(output, h=profile.denoise_strength * strength)
    elif profile.denoise_method == "bilateral":
        output = apply_denoise_bilateral(output, strength=profile.denoise_strength * strength)

    sigma = (
        sigma_from_kernel_size(profile.kernel_size)
        if profile.use_auto_sigma
        else profile.sigma
    )
    output = high_boost_filter(
        image=output,
        sharpening_factor=profile.sharpening_factor * strength,
        kernel_size=profile.kernel_size,
        sigma=sigma,
    )

    if profile.use_clahe:
        output = apply_clahe(
            output,
            clip_limit=profile.clahe_clip_limit,
            tile_grid_size=profile.clahe_tile_grid_size,
        )

    output = recover_details_unsharp(
        reference_image=image,
        target_image=output,
        amount=profile.detail_recovery_amount * strength,
    )

    if preserve_edges_enabled:
        output = preserve_edges(
            original_image=image,
            processed_image=output,
            strength=min(1.0, 0.6 * strength),
        )

    return output


def encode_jpeg(image: np.ndarray) -> bytes:
    """Codifica a imagem em JPEG para download."""
    success, encoded = cv2.imencode(".jpg", image)
    if not success:
        raise RuntimeError("Falha ao codificar imagem em JPEG.")
    return encoded.tobytes()
