"""NeuraFind application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import (
    SentenceTransformerModel,
)
from src.neurafind.search.hybrid_search_service import HybridSearchService
from src.neurafind.services.embedding_indexing_service import EmbeddingIndexingService
from src.neurafind.ui.main_window import MainWindow

DATABASE_PATH = "neurafind.db"


def main() -> None:
    """Launch the NeuraFind desktop application."""
    app = QApplication(sys.argv)

    # -- Initialise backend services --
    model = SentenceTransformerModel()
    embedding_service = EmbeddingService(model)

    indexing_service = EmbeddingIndexingService(
        database_path=DATABASE_PATH,
        embedding_service=embedding_service,
    )

    search_service = HybridSearchService(
        database_path=DATABASE_PATH,
        embedding_service=embedding_service,
    )

    # -- Show window --
    window = MainWindow(
        indexing_service=indexing_service,
        search_service=search_service,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
