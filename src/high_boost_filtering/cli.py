from __future__ import annotations

import argparse

from .config import DEFAULT_CONFIG
from .pipeline import process_image_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aplica High Boost Filtering em uma imagem.",
    )
    parser.add_argument(
        "--image",
        default=DEFAULT_CONFIG.default_image_filename,
        help="Nome do arquivo em Input_Images",
    )
    parser.add_argument(
        "--k",
        type=float,
        default=DEFAULT_CONFIG.default_sharpening_factor,
        help="Fator de nitidez",
    )
    parser.add_argument(
        "--kernel-size",
        type=int,
        default=DEFAULT_CONFIG.default_kernel_size,
        help="Tamanho do kernel (ímpar)",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=DEFAULT_CONFIG.default_sigma,
        help="Sigma do filtro Gaussiano",
    )
    return parser


def run_cli() -> None:
    args = build_parser().parse_args()
    output_path = process_image_file(
        image_filename=args.image,
        sharpening_factor=args.k,
        kernel_size=args.kernel_size,
        sigma=args.sigma,
        config=DEFAULT_CONFIG,
    )
    print(f"Processamento concluído: {output_path}")
