from pathlib import Path

from src.neurafind.storage.document_store import DocumentStore


class SearchService:
    """Provides exact text search over indexed documents."""

    def __init__(self, database_path: str | Path):
        self.store = DocumentStore(database_path)

    def search(self, query: str, location_filter: str = None) -> list[dict[str, str]]:
        query = query.strip().lower()

        if not query:
            return []

        results = []

        for document in self.store.get_all_documents(location_filter=location_filter):
            content = document["content"].lower()

            if query in content:
                results.append(document)

        return results