"""Model management service for NeuraFind."""

from __future__ import annotations

from pathlib import Path


AVAILABLE_MODELS: dict[str, str] = {
    "models/minilm-onnx": (
        "Fast multilingual ONNX (paraphrase-multilingual-MiniLM-L12-v2)"
    ),
}

DEFAULT_MODEL = "models/minilm-onnx"


def is_model_installed(model_name: str) -> bool:
    """Check whether an ONNX model is available locally."""
    model_path = Path(model_name)

    required_files = [
        model_path / "config.json",
        model_path / "tokenizer.json",
        model_path / "tokenizer_config.json",
        model_path / "special_tokens_map.json",
        model_path / "onnx" / "model_quantized.onnx",
    ]

    return all(path.exists() for path in required_files)


def get_model_path(model_name: str) -> str | None:
    """Return the local model path if installed."""
    if is_model_installed(model_name):
        return str(Path(model_name))

    return None


def download_model(model_name: str) -> str:
    """Model download is handled externally for now."""
    raise RuntimeError(
        "Automatic ONNX model download is not implemented yet. "
        "Please place the ONNX model files in models/minilm-onnx."
    )