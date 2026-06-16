from sentence_transformers import SentenceTransformer

from src.neurafind.embeddings.embedding_model import EmbeddingModel


class SentenceTransformerModel(EmbeddingModel):
    """Embedding model implementation using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()