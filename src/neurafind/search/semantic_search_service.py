from pathlib import Path
from math import sqrt

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.storage.document_store import DocumentStore
from src.neurafind.storage.vector_store import VectorStore


class SemanticSearchService:
    """Provides semantic search using stored document embeddings."""

    def __init__(
        self,
        database_path: str | Path,
        embedding_service: EmbeddingService,
    ):
        self.document_store = DocumentStore(database_path)
        self.vector_store = VectorStore(database_path)
        self.embedding_service = embedding_service

    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

        norm_a = sqrt(sum(a * a for a in vector_a))
        norm_b = sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def search(self, query: str) -> list[dict]:
        query_embedding = self.embedding_service.embed_text(query)

        results = []

        for document in self.document_store.get_all_documents():
            document_embedding = self.vector_store.get_embedding(document["path"])

            if document_embedding is None:
                continue

            score = self._cosine_similarity(query_embedding, document_embedding)

            result = dict(document)
            result["score"] = score

            results.append(result)

        return sorted(
            results,
            key=lambda item: item["score"],
            reverse=True,
        )