"""NeuraFind main window — PySide6 desktop interface."""

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


# ---------------------------------------------------------------------------
# Background workers
# ---------------------------------------------------------------------------

class _IndexWorker(QThread):
    """Runs folder indexing on a background thread."""

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


class _SearchWorker(QThread):
    """Runs hybrid search on a background thread."""

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, service, query: str):
        super().__init__()
        self._service = service
        self._query = query

    def run(self):
        try:
            results = self._service.search(self._query)
            self.finished.emit(results)
        except Exception as exc:
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

_STYLESHEET = """
QMainWindow {
    background-color: #1e1e2e;
}

QLabel {
    color: #cdd6f4;
}

QLabel#status_label {
    color: #a6adc8;
    padding: 4px 0px;
}

QLabel#folder_label {
    color: #bac2de;
    padding: 2px 4px;
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 4px;
    min-height: 24px;
}

QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    border: 1px solid #585b70;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #585b70;
    border-color: #6c7086;
}

QPushButton:pressed {
    background-color: #313244;
}

QPushButton:disabled {
    background-color: #313244;
    color: #6c7086;
    border-color: #45475a;
}

QPushButton#index_button {
    background-color: #89b4fa;
    color: #1e1e2e;
    border-color: #74c7ec;
    font-weight: 600;
}

QPushButton#index_button:hover {
    background-color: #74c7ec;
}

QPushButton#index_button:pressed {
    background-color: #89dceb;
}

QPushButton#index_button:disabled {
    background-color: #45475a;
    color: #6c7086;
    border-color: #45475a;
}

QPushButton#search_button {
    background-color: #a6e3a1;
    color: #1e1e2e;
    border-color: #94e2d5;
    font-weight: 600;
}

QPushButton#search_button:hover {
    background-color: #94e2d5;
}

QPushButton#search_button:pressed {
    background-color: #89dceb;
}

QPushButton#search_button:disabled {
    background-color: #45475a;
    color: #6c7086;
    border-color: #45475a;
}

QLineEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: #585b70;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QTableWidget {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 6px;
    gridline-color: #313244;
    selection-background-color: #45475a;
    selection-color: #cdd6f4;
}

QTableWidget::item {
    padding: 6px 10px;
}

QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-bottom: 2px solid #45475a;
    padding: 8px 10px;
    font-weight: 600;
}

QScrollBar:vertical {
    background: #181825;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #585b70;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    """NeuraFind desktop interface."""

    def __init__(
        self,
        indexing_service,
        search_service,
    ):
        super().__init__()
        self._indexing_service = indexing_service
        self._search_service = search_service

        self._selected_folder: str | None = None
        self._worker: QThread | None = None

        self._init_ui()

    # ---- UI construction ---------------------------------------------------

    def _init_ui(self) -> None:
        self.setWindowTitle("NeuraFind")
        self.setMinimumSize(860, 560)
        self.resize(960, 640)
        self.setStyleSheet(_STYLESHEET)

        body_font = QFont("Segoe UI", 10)
        self.setFont(body_font)

        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        # -- Title --
        title_label = QLabel("NeuraFind")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root_layout.addWidget(title_label)

        # -- Folder row --
        folder_row = QHBoxLayout()
        folder_row.setSpacing(10)

        self._folder_button = QPushButton("Select Folder")
        self._folder_button.setFixedWidth(130)
        self._folder_button.clicked.connect(self._on_select_folder)
        folder_row.addWidget(self._folder_button)

        self._folder_label = QLabel("No folder selected")
        self._folder_label.setObjectName("folder_label")
        self._folder_label.setMinimumHeight(34)
        folder_row.addWidget(self._folder_label, stretch=1)

        self._index_button = QPushButton("Index")
        self._index_button.setObjectName("index_button")
        self._index_button.setFixedWidth(100)
        self._index_button.setEnabled(False)
        self._index_button.clicked.connect(self._on_index)
        folder_row.addWidget(self._index_button)

        root_layout.addLayout(folder_row)

        # -- Search row --
        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Enter search query…")
        self._search_input.returnPressed.connect(self._on_search)
        search_row.addWidget(self._search_input, stretch=1)

        self._search_button = QPushButton("Search")
        self._search_button.setObjectName("search_button")
        self._search_button.setFixedWidth(100)
        self._search_button.clicked.connect(self._on_search)
        search_row.addWidget(self._search_button)

        root_layout.addLayout(search_row)

        # -- Results table --
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["File Path", "Score", "Source"])
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)

        header = self._table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        root_layout.addWidget(self._table, stretch=1)

        # -- Status bar --
        self._status_label = QLabel("Ready.")
        self._status_label.setObjectName("status_label")
        root_layout.addWidget(self._status_label)

    # ---- Slots -------------------------------------------------------------

    def _on_select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self._selected_folder = folder
            self._folder_label.setText(folder)
            self._index_button.setEnabled(True)
            self._status_label.setText("Folder selected. Click Index to begin.")

    def _on_index(self) -> None:
        if not self._selected_folder:
            return

        self._set_busy(True)
        self._status_label.setText("Indexing… please wait.")

        worker = _IndexWorker(self._indexing_service, self._selected_folder)
        worker.finished.connect(self._on_index_finished)
        worker.error.connect(self._on_worker_error)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        self._worker = worker
        worker.start()

    def _on_index_finished(self, count: int) -> None:
        self._set_busy(False)
        self._status_label.setText(f"Indexing complete — {count} document(s) indexed.")

    def _on_search(self) -> None:
        query = self._search_input.text().strip()
        if not query:
            return

        self._set_busy(True)
        self._status_label.setText("Searching…")

        worker = _SearchWorker(self._search_service, query)
        worker.finished.connect(self._on_search_finished)
        worker.error.connect(self._on_worker_error)
        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        self._worker = worker
        worker.start()

    def _on_search_finished(self, results: list) -> None:
        self._set_busy(False)
        self._populate_table(results)
        self._status_label.setText(f"Search complete — {len(results)} result(s).")

    def _on_worker_error(self, message: str) -> None:
        self._set_busy(False)
        self._status_label.setText(f"Error: {message}")

    # ---- Helpers -----------------------------------------------------------

    def _set_busy(self, busy: bool) -> None:
        self._folder_button.setEnabled(not busy)
        self._index_button.setEnabled(not busy and self._selected_folder is not None)
        self._search_button.setEnabled(not busy)
        self._search_input.setEnabled(not busy)

    def _populate_table(self, results: list[dict]) -> None:
        self._table.setRowCount(0)
        self._table.setRowCount(len(results))

        for row, result in enumerate(results):
            path_item = QTableWidgetItem(str(result.get("path", "")))
            score_item = QTableWidgetItem(f'{result.get("score", 0):.4f}')
            source_item = QTableWidgetItem(str(result.get("source", "")))

            score_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            source_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self._table.setItem(row, 0, path_item)
            self._table.setItem(row, 1, score_item)
            self._table.setItem(row, 2, source_item)
