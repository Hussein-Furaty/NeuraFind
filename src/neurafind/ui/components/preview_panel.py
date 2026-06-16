"""Preview Panel component (bottom or right)."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit,
)


class PreviewPanel(QWidget):
    """Shows metadata and text preview for a selected result."""

    def __init__(self) -> None:
        super().__init__()
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("preview_header")
        header.setFixedHeight(28)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(12, 0, 8, 0)
        title = QLabel("PREVIEW")
        title.setObjectName("panel_title")
        hl.addWidget(title)
        hl.addStretch()
        layout.addWidget(header)

        # Metadata area
        meta = QWidget()
        ml = QVBoxLayout(meta)
        ml.setContentsMargins(14, 10, 14, 6)
        ml.setSpacing(4)

        self._name_lbl = QLabel("--")
        self._name_lbl.setObjectName("section_title")
        self._name_lbl.setWordWrap(True)
        ml.addWidget(self._name_lbl)

        # Field rows
        fields_layout = QHBoxLayout()
        fields_layout.setSpacing(24)

        for attr, label in [
            ("_type_lbl", "Type"),
            ("_score_lbl", "Score"),
            ("_source_lbl", "Source"),
        ]:
            col = QVBoxLayout()
            col.setSpacing(1)
            fl = QLabel(label)
            fl.setObjectName("field_label")
            col.addWidget(fl)
            vl = QLabel("--")
            vl.setObjectName("field_value")
            setattr(self, attr, vl)
            col.addWidget(vl)
            fields_layout.addLayout(col)

        fields_layout.addStretch()
        ml.addLayout(fields_layout)

        # Path
        path_row = QHBoxLayout()
        path_row.setSpacing(6)
        pl = QLabel("Path:")
        pl.setObjectName("field_label")
        pl.setFixedWidth(36)
        path_row.addWidget(pl)
        self._path_lbl = QLabel("--")
        self._path_lbl.setObjectName("field_value")
        self._path_lbl.setWordWrap(True)
        self._path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        path_row.addWidget(self._path_lbl, stretch=1)
        ml.addLayout(path_row)

        layout.addWidget(meta)

        # Text preview
        self._text_preview = QPlainTextEdit()
        self._text_preview.setReadOnly(True)
        self._text_preview.setPlaceholderText("Select a result to see its content here.")
        layout.addWidget(self._text_preview, stretch=1)

    def show_result(self, result: dict) -> None:
        filepath = str(result.get("path", ""))
        p = Path(filepath) if filepath else None

        self._name_lbl.setText(p.name if p else "--")
        self._path_lbl.setText(filepath or "--")
        ext = p.suffix.upper().lstrip(".") if p and p.suffix else "FILE"
        self._type_lbl.setText(ext)
        self._score_lbl.setText(f'{result.get("score", 0):.4f}')
        self._source_lbl.setText(str(result.get("source", "--")).capitalize())

        content = result.get("content", "") or result.get("text", "")
        self._text_preview.setPlainText(content[:5000] if content else "No text preview available.")

    def clear_preview(self) -> None:
        self._name_lbl.setText("--")
        self._path_lbl.setText("--")
        self._type_lbl.setText("--")
        self._score_lbl.setText("--")
        self._source_lbl.setText("--")
        self._text_preview.clear()
