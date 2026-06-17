"""NeuraFind application entry point."""

import os
import sys
from pathlib import Path

from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QApplication

from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.onnx_embedding_model import ONNXEmbeddingModel
from src.neurafind.search.hybrid_search_service import HybridSearchService
from src.neurafind.services.embedding_indexing_service import EmbeddingIndexingService
from src.neurafind.services.model_service import DEFAULT_MODEL, get_model_path, is_model_installed
from src.neurafind.ui.main_window import MainWindow

def _get_db_path() -> str:
    app_data = Path(os.getenv("LOCALAPPDATA", Path.home() / ".local" / "share"))
    neura_dir = app_data / "NeuraFind"
    neura_dir.mkdir(parents=True, exist_ok=True)
    return str(neura_dir / "neurafind.db")

DATABASE_PATH = _get_db_path()


class _App:
    """Application controller that wires services and handles model swaps."""

    def __init__(self):
        self._model_name = DEFAULT_MODEL
        self._embedding_service: EmbeddingService | None = None
        self._indexing_service: EmbeddingIndexingService | None = None
        self._search_service: HybridSearchService | None = None
        self._window: MainWindow | None = None

    def _init_services(self) -> None:
        """Initialise backend services with the current ONNX model."""
        if is_model_installed(self._model_name):
            model_path = get_model_path(self._model_name)
            model = ONNXEmbeddingModel(model_path)
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

        if self._window is not None:
            self._window._search_service = self._search_service
            self._window._indexing_service = self._indexing_service

    def run(self) -> int:
        app = QApplication(sys.argv)

        from src.neurafind.ui.splash import show_splash

        self.splash = show_splash()

        self._services_ready = False
        self._time_elapsed = False

        self._worker = _InitWorker(self)
        self._worker.finished.connect(self._mark_services_ready)
        self._worker.start()

        QTimer.singleShot(2500, self._mark_time_elapsed)

        return app.exec()

    def _mark_services_ready(self):
        self._services_ready = True
        self._check_ready()

    def _mark_time_elapsed(self):
        self._time_elapsed = True
        self._check_ready()

    def _check_ready(self):
        if self._services_ready and self._time_elapsed:
            self._window = MainWindow(
                indexing_service=self._indexing_service,
                search_service=self._search_service,
                model_name=self._model_name,
                on_model_changed=self.on_model_changed,
            )
            self._window.show()
            self.splash.finish(self._window)


class _InitWorker(QThread):
    finished = Signal()

    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller

    def run(self):
        self.app_controller._init_services()
        self.finished.emit()


class _PlaceholderModel:
    """Stand-in embedding model used when the real model is not available."""

    def __init__(self, model_name: str):
        self._model_name = model_name

    def embed(self, text: str) -> list[float]:
        raise RuntimeError(
            f"Embedding model '{self._model_name}' is not installed. "
            f"Please place the ONNX model files in models/minilm-onnx."
        )


def main() -> None:
    """Launch the NeuraFind desktop application."""
    application = _App()
    sys.exit(application.run())


if __name__ == "__main__":
    main()