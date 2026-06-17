"""Background QThread workers for non-blocking UI."""

from PySide6.QtCore import QThread, Signal

class IndexWorker(QThread):
    finished = Signal(int)
    error = Signal(str)

    def __init__(self, service, folder_path: str):
        super().__init__()
        self._service = service
        self._folder_path = folder_path

    def run(self):
        try:
            count = self._service.index_folder(self._folder_path)
            self.finished.emit(count)
        except Exception as exc:
            self.error.emit(str(exc))

class SearchWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, service, query: str, top_k: int = 10, location_filter: str = None):
        super().__init__()
        self._service = service
        self._query = query
        self._top_k = top_k
        self._location_filter = location_filter

    def run(self):
        try:
            results = self._service.search(
                self._query, 
                top_k=self._top_k, 
                location_filter=self._location_filter
            )

            self.finished.emit(results)
        except Exception as exc:
            self.error.emit(str(exc))

class ModelDownloadWorker(QThread):
    finished = Signal(str)
    error = Signal(str)
    progress = Signal(int) # Currently unused, but good practice

    def __init__(self, model_name: str):
        super().__init__()
        self._model_name = model_name

    def run(self):
        try:
            from src.neurafind.services.model_service import download_model
            download_model(self._model_name)
            self.finished.emit(self._model_name)
        except Exception as exc:
            self.error.emit(str(exc))
