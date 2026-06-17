from pathlib import Path
from math import sqrt

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.storage.document_store import DocumentStore
from src.neurafind.storage.vector_store import VectorStore
from src.neurafind.config import MIN_SIMILARITY_SCORE


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

    def search(
        self,
        query: str,
        top_k: int = 10,
        min_score: float | None = None,
        adaptive: bool = True,
        location_filter: str = None,
    ) -> list[dict]:
        query = query.strip()

        if not query:
            return []

        query_embedding = self.embedding_service.embed_text(query)

        # Use configured default if no explicit min_score provided
        if min_score is None:
            min_score = MIN_SIMILARITY_SCORE

        results = []

        for document in self.document_store.get_all_documents(location_filter=location_filter):
            document_embedding = self.vector_store.get_embedding(document["path"])

            if document_embedding is None:
                continue

            score = self._cosine_similarity(query_embedding, document_embedding)

            results.append({**document, "score": score})

        # Adaptive threshold: boost min_score based on top result similarity
        if adaptive and results:
            top_score = max(r["score"] for r in results)
            # Use 70% of the best score as dynamic floor (but never lower than configured default)
            adaptive_min = max(min_score, top_score * 0.7)
            results = [r for r in results if r["score"] >= adaptive_min]
        else:
            results = [r for r in results if r["score"] >= min_score]

        ranked_results = sorted(
            results,
            key=lambda item: item["score"],
            reverse=True,
        )

        return ranked_results[:top_k]