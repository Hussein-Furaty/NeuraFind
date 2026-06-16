"""Quick Search floating dialog (Ctrl+K)."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QLabel, QWidget,
)

from src.neurafind.ui.core.state import state


class QuickSearchDialog(QDialog):
    """Floating Raycast-style quick search."""

    search_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(550, 380)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        container = QWidget()
        container.setObjectName("quick_search_container")
        cl = QVBoxLayout(container)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        self._input = QLineEdit()
        self._input.setObjectName("quick_search_input")
        self._input.setPlaceholderText("Search documents... (Enter)")
        self._input.setFixedHeight(50)
        self._input.returnPressed.connect(self._on_search)
        self._input.textChanged.connect(self._filter_history)
        cl.addWidget(self._input)

        lbl = QLabel("  Recent Searches")
        lbl.setObjectName("field_label")
        lbl.setFixedHeight(28)
        cl.addWidget(lbl)

        self._history_list = QListWidget()
        self._history_list.itemClicked.connect(self._on_history_clicked)
        cl.addWidget(self._history_list)

        layout.addWidget(container)

    def showEvent(self, event):
        self._input.clear()
        self._populate_history()
        self._input.setFocus()
        super().showEvent(event)

    def _populate_history(self, filter_text=""):
        self._history_list.clear()
        for h in state.search_history:
            if not filter_text or filter_text.lower() in h.lower():
                self._history_list.addItem(h)

    def _filter_history(self, text):
        self._populate_history(text)

    def _on_search(self):
        query = self._input.text().strip()
        if query:
            self.search_requested.emit(query)
            self.accept()

    def _on_history_clicked(self, item):
        self.search_requested.emit(item.text())
        self.accept()
