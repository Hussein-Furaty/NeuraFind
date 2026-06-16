"""NeuraFind Main Window — IDE-style shell assembling all components."""

import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QStatusBar, QApplication, QProgressBar, QFileDialog,
    QMenu,
)

from src.neurafind.ui.core.theme import get_theme, build_stylesheet
from src.neurafind.ui.core.state import state
from src.neurafind.ui.core.workers import IndexWorker, SearchWorker

from src.neurafind.ui.components.explorer import FileExplorer
from src.neurafind.ui.components.workspace import Workspace
from src.neurafind.ui.components.preview_panel import PreviewPanel
from src.neurafind.ui.components.quick_search import QuickSearchDialog
from src.neurafind.ui.components.notifications import ToastNotification

from src.neurafind.ui.dialogs.settings import SettingsDialog
from src.neurafind.ui.dialogs.about import AboutDialog
from src.neurafind.ui.dialogs.indexing import IndexingManagerDialog


def _assets_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent / "assets"


def _icon_path() -> str:
    return str(_assets_dir() / "NeuraFind.ico")


def _logo_path() -> str:
    return str(_assets_dir() / "neurafind-logo.png")


def _open_file(filepath: str) -> None:
    """Open a file with the default system application."""
    p = Path(filepath)
    if not p.exists():
        return
    if sys.platform == "win32":
        os.startfile(str(p))
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(p)])
    else:
        subprocess.Popen(["xdg-open", str(p)])


def _open_folder(filepath: str) -> None:
    """Open the containing folder and select the file."""
    p = Path(filepath)
    if sys.platform == "win32":
        if p.exists():
            subprocess.Popen(["explorer", "/select,", str(p)])
        elif p.parent.exists():
            subprocess.Popen(["explorer", str(p.parent)])
    elif sys.platform == "darwin":
        if p.exists():
            subprocess.Popen(["open", "-R", str(p)])
    else:
        folder = str(p.parent) if p.parent.exists() else str(p)
        subprocess.Popen(["xdg-open", folder])


class MainWindow(QMainWindow):
    """IDE-style main window assembling all NeuraFind components."""

    def __init__(self, indexing_service, search_service, model_name: str, on_model_changed=None):
        super().__init__()
        self._indexing_service = indexing_service
        self._search_service = search_service
        self._model_name = model_name
        self._on_model_changed_cb = on_model_changed

        self._selected_location: str | None = None
        self._current_results: list[dict] = []
        self._workers: list = []

        self._init_ui()

    # ── UI Construction ──────────────────────────────────────────

    def _init_ui(self) -> None:
        self.setWindowTitle("NeuraFind - Document Intelligence")
        self.setMinimumSize(1100, 700)
        self.resize(1300, 800)

        ico = _icon_path()
        if os.path.exists(ico):
            self.setWindowIcon(QIcon(ico))

        self._apply_theme()
        self._build_menubar()
        self._build_toolbar()
        self._build_statusbar()
        self._build_central()

    def _apply_theme(self) -> None:
        t = get_theme(state.settings.get("theme", "dark"))
        sheet = build_stylesheet(t)
        self.setStyleSheet(sheet)

    def _build_menubar(self) -> None:
        bar = self.menuBar()

        # File
        fm = bar.addMenu("&File")
        a = fm.addAction("Select Location...")
        a.setShortcut("Ctrl+O")
        a.triggered.connect(self._on_browse_folder)
        fm.addSeparator()
        a = fm.addAction("Exit")
        a.setShortcut("Alt+F4")
        a.triggered.connect(self.close)

        # Edit
        em = bar.addMenu("&Edit")
        a = em.addAction("Quick Search...")
        a.setShortcut("Ctrl+K")
        a.triggered.connect(self._open_quick_search)

        # View
        vm = bar.addMenu("&View")
        a = vm.addAction("Toggle Explorer")
        a.setShortcut("Ctrl+B")
        a.triggered.connect(self._toggle_explorer)
        a = vm.addAction("Toggle Preview")
        a.setShortcut("Ctrl+J")
        a.triggered.connect(self._toggle_preview)

        # Tools
        tm = bar.addMenu("&Tools")
        a = tm.addAction("Index Current Location")
        a.setShortcut("Ctrl+I")
        a.triggered.connect(self._on_index)
        a = tm.addAction("Focus Search")
        a.setShortcut("Ctrl+F")
        a.triggered.connect(self._focus_search)
        tm.addSeparator()
        a = tm.addAction("Indexing Manager...")
        a.triggered.connect(self._open_indexing)
        a = tm.addAction("Settings...")
        a.setShortcut("Ctrl+,")
        a.triggered.connect(self._open_settings)

        # Help
        hm = bar.addMenu("&Help")
        a = hm.addAction("About NeuraFind")
        a.setShortcut("F1")
        a.triggered.connect(self._open_about)

    def _build_toolbar(self) -> None:
        tb = self.addToolBar("Main")
        tb.setMovable(False)
        tb.setFloatable(False)
        tb.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

        # Brand
        brand = QWidget()
        bl = QHBoxLayout(brand)
        bl.setContentsMargins(8, 0, 14, 0)
        bl.setSpacing(6)

        logo = _logo_path()
        if os.path.exists(logo):
            logo_lbl = QLabel()
            pm = QPixmap(logo).scaled(
                18, 18,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl.setPixmap(pm)
            bl.addWidget(logo_lbl)

        name_lbl = QLabel("NeuraFind")
        name_lbl.setObjectName("section_title")
        bl.addWidget(name_lbl)

        tb.addWidget(brand)
        tb.addSeparator()

        tb.addAction("Select Location", self._on_browse_folder)
        tb.addAction("Index", self._on_index)
        tb.addAction("Search", self._focus_search)
        tb.addSeparator()
        tb.addAction("Settings", self._open_settings)
        tb.addAction("About", self._open_about)

    def _build_statusbar(self) -> None:
        self._sb = QStatusBar()
        self.setStatusBar(self._sb)

        self._prog = QProgressBar()
        self._prog.setFixedWidth(160)
        self._prog.setRange(0, 0)
        self._prog.setVisible(False)
        self._sb.addPermanentWidget(self._prog)

        self._sb.showMessage("Ready")

    def _build_central(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Horizontal splitter: explorer | workspace+preview
        self._h_split = QSplitter(Qt.Orientation.Horizontal)

        # Left: File Explorer
        self._explorer = FileExplorer()
        self._explorer.location_selected.connect(self._on_location_selected)
        self._h_split.addWidget(self._explorer)

        # Right: Vertical splitter (workspace on top, preview on bottom)
        self._v_split = QSplitter(Qt.Orientation.Vertical)

        # Workspace
        self._workspace = Workspace()
        self._workspace.search_requested.connect(self._on_search)
        self._workspace.index_requested.connect(self._on_index)
        self._workspace.action_open_file.connect(self._handle_open_file)
        self._workspace.action_open_folder.connect(self._handle_open_folder)
        self._workspace.action_copy_path.connect(self._handle_copy_path)
        self._workspace.action_preview.connect(self._handle_preview)
        self._v_split.addWidget(self._workspace)

        # Preview
        self._preview = PreviewPanel()
        self._v_split.addWidget(self._preview)

        self._v_split.setSizes([550, 200])
        self._h_split.addWidget(self._v_split)
        self._h_split.setSizes([250, 1050])

        lay.addWidget(self._h_split)

    # ── Slots ────────────────────────────────────────────────────

    @Slot(str)
    def _on_location_selected(self, path: str) -> None:
        self._selected_location = path
        self._workspace.set_location(path)
        self._sb.showMessage(f"Location: {path}")

    def _on_browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Location")
        if folder:
            self._on_location_selected(folder)

    def _focus_search(self) -> None:
        self._workspace.focus_search()

    def _toggle_explorer(self) -> None:
        self._explorer.setVisible(not self._explorer.isVisible())

    def _toggle_preview(self) -> None:
        self._preview.setVisible(not self._preview.isVisible())

    def _open_quick_search(self) -> None:
        dlg = QuickSearchDialog(self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.search_requested.connect(self._on_search)
        dlg.exec()

    def _open_settings(self) -> None:
        dlg = SettingsDialog(self._model_name, self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.settings_changed.connect(self._on_settings_changed)
        dlg.model_changed.connect(self._on_model_changed)
        dlg.exec()

    def _on_settings_changed(self) -> None:
        self._apply_theme()

    @Slot(str)
    def _on_model_changed(self, name: str) -> None:
        self._model_name = name
        if self._on_model_changed_cb:
            self._on_model_changed_cb(name)
        self._sb.showMessage(f"Model changed to: {name}")
        self._show_toast(f"Model activated: {name}", "success")

    def _open_indexing(self) -> None:
        dlg = IndexingManagerDialog(self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.exec()

    def _open_about(self) -> None:
        dlg = AboutDialog(self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.exec()

    # ── Toasts ───────────────────────────────────────────────────

    def _show_toast(self, msg: str, type_: str = "info") -> None:
        toast = ToastNotification(self, msg, type_)
        toast.show_toast()

    # ── Worker: Index ────────────────────────────────────────────

    def _set_busy(self, busy: bool) -> None:
        self._prog.setVisible(busy)
        self._workspace.set_busy(busy)

    def _on_index(self) -> None:
        if not self._selected_location:
            self._sb.showMessage("Please select a folder first.")
            self._show_toast("Select a folder in the Explorer first.", "warning")
            return

        self._set_busy(True)
        self._sb.showMessage(f"Indexing {self._selected_location}...")

        w = IndexWorker(self._indexing_service, self._selected_location)
        w.finished.connect(self._on_index_done)
        w.error.connect(self._on_index_err)
        w.finished.connect(w.deleteLater)
        w.error.connect(w.deleteLater)
        self._workers.append(w)
        w.start()

    @Slot(int)
    def _on_index_done(self, count: int) -> None:
        self._set_busy(False)
        self._sb.showMessage(f"Indexed {count} documents successfully.")
        self._show_toast(f"Indexing complete: {count} documents.", "success")

    @Slot(str)
    def _on_index_err(self, err: str) -> None:
        self._set_busy(False)
        self._sb.showMessage(f"Indexing error: {err}")
        self._show_toast(f"Indexing failed: {err}", "error")

    # ── Worker: Search ───────────────────────────────────────────

    @Slot(str)
    def _on_search(self, query: str) -> None:
        self._set_busy(True)
        self._sb.showMessage(f"Searching: {query}")

        limit = state.settings.get("result_limit", 50)
        # Pass the selected location so the worker filters the results properly
        w = SearchWorker(self._search_service, query, top_k=limit, location_filter=self._selected_location)
        w.finished.connect(self._on_search_done)
        w.error.connect(self._on_search_err)
        w.finished.connect(w.deleteLater)
        w.error.connect(w.deleteLater)
        self._workers.append(w)
        w.start()

    @Slot(list)
    def _on_search_done(self, results: list) -> None:
        self._set_busy(False)
        self._current_results = results
        self._workspace.set_results(results)
        n = len(results)
        self._sb.showMessage(f"Search complete: {n} result(s)")
        self._show_toast(f"Found {n} results.", "success")

    @Slot(str)
    def _on_search_err(self, err: str) -> None:
        self._set_busy(False)
        self._sb.showMessage(f"Search error: {err}")
        self._show_toast(f"Search failed: {err}", "error")

    # ── Result Actions ───────────────────────────────────────────

    def _handle_open_file(self, path: str) -> None:
        _open_file(path)

    def _handle_open_folder(self, path: str) -> None:
        _open_folder(path)

    def _handle_copy_path(self, path: str) -> None:
        QApplication.clipboard().setText(path)
        self._sb.showMessage("Path copied.")
        self._show_toast("Path copied to clipboard.", "info")

    def _handle_preview(self, result: dict) -> None:
        self._preview.show_result(result)
        if not self._preview.isVisible():
            self._preview.setVisible(True)
