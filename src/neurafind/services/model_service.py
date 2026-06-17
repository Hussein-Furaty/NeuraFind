"""Model management service for NeuraFind."""

from __future__ import annotations

import sys
from pathlib import Path


MODEL_ID = "minilm-onnx"

AVAILABLE_MODELS: dict[str, str] = {
    MODEL_ID: "Fast multilingual ONNX (paraphrase-multilingual-MiniLM-L12-v2)",
}

DEFAULT_MODEL = MODEL_ID


def _app_base_dir() -> Path:
    """Return base directory for source mode and PyInstaller mode."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    return Path.cwd()


def get_model_path(model_name: str) -> str | None:
    """Return the local model path if installed."""
    model_path = _app_base_dir() / "models" / model_name

    if is_model_installed(model_name):
        return str(model_path)

    return None


def is_model_installed(model_name: str) -> bool:
    """Check whether an ONNX model is available locally."""
    model_path = _app_base_dir() / "models" / model_name

    required_files = [
        model_path / "config.json",
        model_path / "tokenizer.json",
        model_path / "tokenizer_config.json",
        model_path / "special_tokens_map.json",
        model_path / "onnx" / "model_quantized.onnx",
    ]

    return all(path.exists() for path in required_files)


def download_model(model_name: str) -> str:
    """Model download is handled externally for now."""
    raise RuntimeError(
        "Automatic ONNX model download is not implemented yet. "
        "Please place the ONNX model files in the NeuraFind models directory."
    )