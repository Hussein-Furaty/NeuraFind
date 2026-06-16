"""Model management service for NeuraFind."""

from __future__ import annotations

import os
from pathlib import Path

from sentence_transformers import SentenceTransformer


# Supported models with human-readable labels.
AVAILABLE_MODELS: dict[str, str] = {
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": (
        "Fast multilingual (paraphrase-multilingual-MiniLM-L12-v2)"
    ),
    "intfloat/multilingual-e5-base": (
        "Accurate multilingual (multilingual-e5-base)"
    ),
}

DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def _hub_cache_dir() -> Path:
    """Return the Hugging Face Hub cache directory."""
    custom = os.environ.get("HF_HOME") or os.environ.get("TRANSFORMERS_CACHE")
    if custom:
        return Path(custom)
    return Path.home() / ".cache" / "huggingface" / "hub"


def is_model_installed(model_name: str) -> bool:
    """Check whether a model is already cached locally."""
    cache_dir = _hub_cache_dir()
    if not cache_dir.exists():
        return False

    # Hugging Face stores models in directories named like:
    #   models--org--model_name
    safe_name = "models--" + model_name.replace("/", "--")
    model_dir = cache_dir / safe_name

    if not model_dir.exists():
        return False

    # Check that at least one snapshot exists (actual model files)
    snapshots = model_dir / "snapshots"
    if snapshots.exists() and any(snapshots.iterdir()):
        return True

    return False


def get_model_path(model_name: str) -> str | None:
    """Return the cached model directory path, or None if not installed."""
    cache_dir = _hub_cache_dir()
    safe_name = "models--" + model_name.replace("/", "--")
    model_dir = cache_dir / safe_name
    snapshots = model_dir / "snapshots"

    if snapshots.exists():
        # Return the latest snapshot directory
        children = sorted(snapshots.iterdir())
        if children:
            return str(children[-1])

    return None


def download_model(model_name: str) -> str:
    """Download a model and return its cache path.

    This is a blocking call and should be run in a worker thread.
    """
    # SentenceTransformer() downloads the model if not cached.
    SentenceTransformer(model_name)
    path = get_model_path(model_name)
    return path or model_name
