from pathlib import Path

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.indexing.indexer import Indexer
from src.neurafind.storage.document_store import DocumentStore
from src.neurafind.storage.vector_store import VectorStore


class EmbeddingIndexingService:
    """Indexes documents and stores their embeddings."""

    def __init__(
        self,
        database_path: str | Path,
        embedding_service: EmbeddingService,
    ):
        self.indexer = Indexer()
        self.document_store = DocumentStore(database_path)
        self.vector_store = VectorStore(database_path)
        self.embedding_service = embedding_service

    def index_folder(self, folder_path: str | Path) -> int:
        documents = self.indexer.index_folder(folder_path)

        self.document_store.save_documents(documents)

        indexed_count = 0

        for document in documents:
            if "error" in document:
                continue

            embedding = self.embedding_service.embed_text(
                document["content"][:5000]
            )

            self.vector_store.save_embedding(
                document["path"],
                embedding,
            )

            indexed_count += 1

        return indexed_count