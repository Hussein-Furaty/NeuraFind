from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """Base interface for text embedding models."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text input."""
        raise NotImplementedError