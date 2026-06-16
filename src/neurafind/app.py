"""NeuraFind application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import (
    SentenceTransformerModel,
)
from src.neurafind.search.hybrid_search_service import HybridSearchService
from src.neurafind.services.embedding_indexing_service import EmbeddingIndexingService
from src.neurafind.services.model_service import DEFAULT_MODEL, is_model_installed
from src.neurafind.ui.main_window import MainWindow

DATABASE_PATH = "neurafind.db"


class _App:
    """Application controller that wires services and handles model swaps."""

    def __init__(self):
        self._model_name = DEFAULT_MODEL
        self._embedding_service: EmbeddingService | None = None
        self._indexing_service: EmbeddingIndexingService | None = None
        self._search_service: HybridSearchService | None = None

        self._init_services()

    def _init_services(self) -> None:
        """Initialise backend services with the current model.

        If the model is not installed the services are created with a
        placeholder that will fail gracefully at search/index time rather
        than crashing at startup.
        """
        if is_model_installed(self._model_name):
            model = SentenceTransformerModel(self._model_name)
        else:
            model = _PlaceholderModel(self._model_name)

        self._embedding_service = EmbeddingService(model)

        self._indexing_service = EmbeddingIndexingService(
            database_path=DATABASE_PATH,
            embedding_service=self._embedding_service,
        )

        self._search_service = HybridSearchService(
            database_path=DATABASE_PATH,
            embedding_service=self._embedding_service,
        )

    def on_model_changed(self, model_name: str) -> None:
        """Rebuild services when the user selects a different model."""
        self._model_name = model_name
        self._init_services()

        # Patch the running window references so the next action uses the
        # new services.
        if self._window is not None:
            self._window._search_service = self._search_service
            self._window._indexing_service = self._indexing_service

    def run(self) -> int:
        app = QApplication(sys.argv)
        
        from src.neurafind.ui.splash import show_splash
        splash = show_splash()
        
        # Give splash a moment to render while we do final setup
        app.processEvents()

        self._window = MainWindow(
            indexing_service=self._indexing_service,
            search_service=self._search_service,
            model_name=self._model_name,
            on_model_changed=self.on_model_changed,
        )
        
        # Simulate loading if it was too fast so user actually sees the premium splash
        import time
        time.sleep(1.0)
        
        self._window.show()
        splash.finish(self._window)

        return app.exec()


class _PlaceholderModel:
    """Stand-in embedding model used when the real model is not yet downloaded.

    Raises a clear error instead of crashing at startup.
    """

    def __init__(self, model_name: str):
        self._model_name = model_name

    def embed(self, text: str) -> list[float]:
        raise RuntimeError(
            f"Embedding model '{self._model_name}' is not installed. "
            f"Please download it from the Settings page first."
        )


def main() -> None:
    """Launch the NeuraFind desktop application."""
    application = _App()
    sys.exit(application.run())


if __name__ == "__main__":
    main()
