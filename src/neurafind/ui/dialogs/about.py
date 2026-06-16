"""Academic About Dialog."""

import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
)


def _logo_path() -> str:
    return str(
        Path(__file__).resolve().parent.parent.parent.parent.parent
        / "assets" / "neurafind-logo.png"
    )


class AboutDialog(QDialog):
    """Formal academic About page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About NeuraFind")
        self.setFixedSize(500, 480)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 24)
        layout.setSpacing(12)

        # Logo
        logo = _logo_path()
        if os.path.exists(logo):
            lbl = QLabel()
            pm = QPixmap(logo).scaled(
                64, 64,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            lbl.setPixmap(pm)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        title = QLabel("NeuraFind")
        title.setObjectName("heading")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        sub = QLabel("Offline Semantic Document Search Platform")
        sub.setObjectName("subheading")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        features = QLabel(
            "Features:\n\n"
            "\u2022  Local-first, Privacy-first\n"
            "\u2022  Semantic & Hybrid Search\n"
            "\u2022  PDF, DOCX, XLSX, PPTX Support\n"
            "\u2022  Local Embedding Models\n"
            "\u2022  Exact, Fuzzy, Semantic, and Hybrid Search"
        )
        features.setObjectName("field_value")
        layout.addWidget(features, stretch=1)

        ver = QLabel("Version 2.0.0  |  github.com/Hussein-Furaty/NeuraFind")
        ver.setObjectName("dim_label")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ver)

        br = QHBoxLayout()
        br.addStretch()
        cb = QPushButton("Close")
        cb.setFixedWidth(90)
        cb.clicked.connect(self.accept)
        br.addWidget(cb)
        layout.addLayout(br)
