from pathlib import Path

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.search.fuzzy_search_service import FuzzySearchService
from src.neurafind.search.search_service import SearchService
from src.neurafind.search.semantic_search_service import SemanticSearchService


class HybridSearchService:
    """Combines exact, fuzzy, and semantic search results."""

    def __init__(
        self,
        database_path: str | Path,
        embedding_service: EmbeddingService,
    ):
        self.exact_search = SearchService(database_path)
        self.fuzzy_search = FuzzySearchService(database_path)
        self.semantic_search = SemanticSearchService(
            database_path=database_path,
            embedding_service=embedding_service,
        )

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        combined_results: dict[str, dict] = {}

        for result in self.exact_search.search(query):
            path = result["path"]
            combined_results[path] = {
                **result,
                "score": 1.0,
                "source": "exact",
            }

        for result in self.fuzzy_search.search(query):
            path = result["path"]
            score = float(result["score"]) / 100

            if path not in combined_results or score > combined_results[path]["score"]:
                combined_results[path] = {
                    **result,
                    "score": score,
                    "source": "fuzzy",
                }

        for result in self.semantic_search.search(query, top_k=top_k):
            path = result["path"]
            score = float(result["score"])

            if path not in combined_results or score > combined_results[path]["score"]:
                combined_results[path] = {
                    **result,
                    "score": score,
                    "source": "semantic",
                }

        ranked_results = sorted(
            combined_results.values(),
            key=lambda item: item["score"],
            reverse=True,
        )

        return ranked_results[:top_k]