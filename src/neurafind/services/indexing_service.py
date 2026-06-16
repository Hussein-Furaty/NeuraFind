from pathlib import Path

from src.neurafind.indexing.indexer import Indexer
from src.neurafind.storage.document_store import DocumentStore


class IndexingService:
    """Coordinates document indexing and storage."""

    def __init__(self, database_path: str | Path):
        self.indexer = Indexer()
        self.store = DocumentStore(database_path)

    def index_folder(self, folder_path: str | Path) -> int:
        documents = self.indexer.index_folder(folder_path)
        self.store.save_documents(documents)

        return len([document for document in documents if "error" not in document])