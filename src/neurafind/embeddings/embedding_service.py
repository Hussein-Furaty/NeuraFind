from src.neurafind.embeddings.embedding_model import EmbeddingModel


class EmbeddingService:
    """Provides a stable interface for generating text embeddings."""

    def __init__(self, model: EmbeddingModel):
        self.model = model

    def embed_text(self, text: str) -> list[float]:
        text = text.strip()

        if not text:
            return []

        return self.model.embed(text)