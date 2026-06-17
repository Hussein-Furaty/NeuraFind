from pathlib import Path

from rapidfuzz import fuzz

from src.neurafind.storage.document_store import DocumentStore


class FuzzySearchService:
    """Provides fuzzy text search over indexed documents."""

    def __init__(self, database_path: str | Path, threshold: int = 70):
        self.store = DocumentStore(database_path)
        self.threshold = threshold

    def search(self, query: str, location_filter: str = None) -> list[dict[str, str]]:
        query = query.strip().lower()

        if not query:
            return []

        results = []

        for document in self.store.get_all_documents(location_filter=location_filter):
            content = document["content"].lower()
            score = fuzz.partial_ratio(query, content)

            if score >= self.threshold:
                result = dict(document)
                result["score"] = str(score)
                results.append(result)

        return sorted(results, key=lambda item: float(item["score"]), reverse=True)