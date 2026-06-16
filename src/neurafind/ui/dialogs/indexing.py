"""Indexing Management Dialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QProgressBar, QListWidget
)

class IndexingManagerDialog(QDialog):
    """Dedicated dialog for managing indexed folders."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Indexing Manager")
        self.setMinimumSize(500, 400)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        lbl = QLabel("Indexing Management")
        lbl.setObjectName("h1")
        layout.addWidget(lbl)
        
        info = QLabel("View and manage currently indexed locations. (Note: currently relies on the main explorer for selection).")
        info.setObjectName("dim_text")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        self._list = QListWidget()
        self._list.addItem("Current indexing locations are managed via the File Explorer.")
        layout.addWidget(self._list, stretch=1)
        
        self._prog = QProgressBar()
        self._prog.setRange(0, 0)
        self._prog.hide()
        layout.addWidget(self._prog)
        
        br = QHBoxLayout()
        br.addStretch()
        cb = QPushButton("Close")
        cb.clicked.connect(self.accept)
        br.addWidget(cb)
        layout.addLayout(br)
