"""Professional IDE-style Settings Dialog."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget,
    QWidget, QLabel, QComboBox, QPushButton, QGroupBox, QSpinBox,
    QDoubleSpinBox, QCheckBox, QProgressBar,
)

from src.neurafind.ui.core.state import state
from src.neurafind.ui.core.workers import ModelDownloadWorker


class SettingsDialog(QDialog):
    """Multi-tab settings dialog."""

    settings_changed = Signal()
    model_changed = Signal(str)

    def __init__(self, current_model: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(720, 520)
        self.resize(750, 550)
        self._current_model = current_model
        self._worker = None
        self._build()

    def _build(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Nav
        self._nav = QListWidget()
        self._nav.setObjectName("settings_nav")
        self._nav.setFixedWidth(160)
        self._nav.addItems(["General", "Search", "Performance", "Models"])
        self._nav.setCurrentRow(0)
        self._nav.currentRowChanged.connect(self._on_page)
        layout.addWidget(self._nav)

        # Stack
        self._stack = QStackedWidget()
        self._build_general()
        self._build_search()
        self._build_perf()
        self._build_models()
        layout.addWidget(self._stack, stretch=1)

    def _on_page(self, row: int) -> None:
        self._stack.setCurrentIndex(row)

    def _make_page(self, title: str) -> QVBoxLayout:
        page = QWidget()
        vl = QVBoxLayout(page)
        vl.setContentsMargins(24, 24, 24, 24)
        vl.setSpacing(16)
        lbl = QLabel(title)
        lbl.setObjectName("heading")
        vl.addWidget(lbl)
        self._stack.addWidget(page)
        return vl

    # ── General ──────────────────────────────────────────────────

    def _build_general(self) -> None:
        vl = self._make_page("General Settings")

        row = QHBoxLayout()
        row.addWidget(QLabel("Theme:"))
        self._theme_cb = QComboBox()
        self._theme_cb.addItems(["dark", "light"])
        self._theme_cb.setCurrentText(state.settings.get("theme", "dark"))
        row.addWidget(self._theme_cb, stretch=1)
        vl.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Language:"))
        self._lang_cb = QComboBox()
        self._lang_cb.addItems(["en", "ar"])
        self._lang_cb.setCurrentText(state.settings.get("language", "en"))
        row2.addWidget(self._lang_cb, stretch=1)
        vl.addLayout(row2)

        vl.addStretch()
        self._add_save_close(vl)

    # ── Search ───────────────────────────────────────────────────

    def _build_search(self) -> None:
        vl = self._make_page("Search Configuration")

        row = QHBoxLayout()
        row.addWidget(QLabel("Result Limit:"))
        self._limit_sb = QSpinBox()
        self._limit_sb.setRange(10, 500)
        self._limit_sb.setValue(state.settings.get("result_limit", 50))
        row.addWidget(self._limit_sb, stretch=1)
        vl.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Semantic Threshold:"))
        self._thresh_sb = QDoubleSpinBox()
        self._thresh_sb.setRange(0.0, 1.0)
        self._thresh_sb.setSingleStep(0.05)
        self._thresh_sb.setValue(state.settings.get("semantic_threshold", 0.65))
        row2.addWidget(self._thresh_sb, stretch=1)
        vl.addLayout(row2)

        vl.addStretch()
        self._add_save_close(vl)

    # ── Performance ──────────────────────────────────────────────

    def _build_perf(self) -> None:
        vl = self._make_page("Performance Options")

        self._cache_chk = QCheckBox("Enable Aggressive Caching")
        self._cache_chk.setChecked(state.settings.get("cache_controls", True))
        vl.addWidget(self._cache_chk)

        vl.addStretch()
        self._add_save_close(vl)

    # ── Models ───────────────────────────────────────────────────

    def _build_models(self) -> None:
        from src.neurafind.services.model_service import (
            AVAILABLE_MODELS, is_model_installed, get_model_path,
        )

        vl = self._make_page("Model Management")

        # Active model info
        grp = QGroupBox("Active Model")
        gl = QVBoxLayout(grp)

        self._m_name_lbl = QLabel(f"Model: {self._current_model}")
        self._m_name_lbl.setObjectName("field_value")
        gl.addWidget(self._m_name_lbl)

        path = get_model_path(self._current_model) or "--"
        self._m_path_lbl = QLabel(f"Path: {path}")
        self._m_path_lbl.setObjectName("field_label")
        self._m_path_lbl.setWordWrap(True)
        self._m_path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        gl.addWidget(self._m_path_lbl)

        vl.addWidget(grp)

        # Change model
        cgrp = QGroupBox("Change Model")
        cgl = QVBoxLayout(cgrp)

        self._model_cb = QComboBox()
        for mid, mlabel in AVAILABLE_MODELS.items():
            self._model_cb.addItem(mlabel, userData=mid)
        idx = self._model_cb.findData(self._current_model)
        if idx >= 0:
            self._model_cb.setCurrentIndex(idx)
        self._model_cb.currentIndexChanged.connect(self._on_model_sel)
        cgl.addWidget(self._model_cb)

        self._m_status_lbl = QLabel("")
        cgl.addWidget(self._m_status_lbl)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self._dl_btn = QPushButton("Download")
        self._dl_btn.setObjectName("accent_btn")
        self._dl_btn.clicked.connect(self._on_download)
        btn_row.addWidget(self._dl_btn)

        self._apply_btn = QPushButton("Activate")
        self._apply_btn.clicked.connect(self._on_activate)
        btn_row.addWidget(self._apply_btn)
        btn_row.addStretch()
        cgl.addLayout(btn_row)

        self._dl_prog = QProgressBar()
        self._dl_prog.setRange(0, 0)
        self._dl_prog.setVisible(False)
        cgl.addWidget(self._dl_prog)

        vl.addWidget(cgrp)

        note = QLabel("Note: Models are downloaded once and then run entirely offline on your machine.")
        note.setObjectName("dim_label")
        note.setWordWrap(True)
        vl.addWidget(note)

        vl.addStretch()

        br = QHBoxLayout()
        br.addStretch()
        cb = QPushButton("Close")
        cb.setFixedWidth(90)
        cb.clicked.connect(self.accept)
        br.addWidget(cb)
        vl.addLayout(br)

        # Initial refresh
        self._on_model_sel()

    # ── Helpers ──────────────────────────────────────────────────

    def _add_save_close(self, layout: QVBoxLayout) -> None:
        br = QHBoxLayout()
        br.addStretch()
        btn = QPushButton("Save && Close")
        btn.setObjectName("accent_btn")
        btn.setFixedWidth(120)
        btn.clicked.connect(self._save_and_close)
        br.addWidget(btn)
        layout.addLayout(br)

    def _save_and_close(self) -> None:
        state.settings["theme"] = self._theme_cb.currentText()
        state.settings["language"] = self._lang_cb.currentText()
        state.settings["result_limit"] = self._limit_sb.value()
        state.settings["semantic_threshold"] = self._thresh_sb.value()
        state.settings["cache_controls"] = self._cache_chk.isChecked()
        state.save()
        self.settings_changed.emit()
        self.accept()

    def _on_model_sel(self) -> None:
        from src.neurafind.services.model_service import is_model_installed

        mid = self._model_cb.currentData()
        if not mid:
            return
        if is_model_installed(mid):
            self._m_status_lbl.setText("Status: Installed")
            self._m_status_lbl.setObjectName("success_label")
            self._dl_btn.setEnabled(False)
            self._apply_btn.setEnabled(mid != self._current_model)
        else:
            self._m_status_lbl.setText("Status: Not Installed")
            self._m_status_lbl.setObjectName("error_label")
            self._dl_btn.setEnabled(True)
            self._apply_btn.setEnabled(False)
        self._m_status_lbl.style().unpolish(self._m_status_lbl)
        self._m_status_lbl.style().polish(self._m_status_lbl)

    def _on_download(self) -> None:
        mid = self._model_cb.currentData()
        if not mid:
            return
        self._dl_btn.setEnabled(False)
        self._dl_prog.setVisible(True)
        self._m_status_lbl.setText("Downloading... Please wait.")
        self._m_status_lbl.setObjectName("")
        self._m_status_lbl.style().unpolish(self._m_status_lbl)
        self._m_status_lbl.style().polish(self._m_status_lbl)

        self._worker = ModelDownloadWorker(mid)
        self._worker.finished.connect(self._on_dl_done)
        self._worker.error.connect(self._on_dl_err)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker.error.connect(self._worker.deleteLater)
        self._worker.start()

    def _on_dl_done(self, _name: str) -> None:
        self._dl_prog.setVisible(False)
        self._on_model_sel()

    def _on_dl_err(self, err: str) -> None:
        self._dl_prog.setVisible(False)
        self._dl_btn.setEnabled(True)
        self._m_status_lbl.setText(f"Error: {err}")
        self._m_status_lbl.setObjectName("error_label")
        self._m_status_lbl.style().unpolish(self._m_status_lbl)
        self._m_status_lbl.style().polish(self._m_status_lbl)

    def _on_activate(self) -> None:
        from src.neurafind.services.model_service import get_model_path

        mid = self._model_cb.currentData()
        if not mid:
            return
        self._current_model = mid
        self._m_name_lbl.setText(f"Model: {mid}")
        self._m_path_lbl.setText(f"Path: {get_model_path(mid) or '--'}")
        self.model_changed.emit(mid)
        self._on_model_sel()
