"""Search Workspace component (Center Panel).

Contains the location bar with Index button, search input,
result count/insights, and the scrollable result card list.
"""

from pathlib import Path
import os
import time
from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QApplication, QSizePolicy,
    QComboBox
)

from src.neurafind.ui.core.state import state


# ── Result Card ──────────────────────────────────────────────────

class _ResultCard(QFrame):
    """A single result card with file info, snippet, and action buttons."""

    open_file = Signal(str)
    open_folder = Signal(str)
    copy_path = Signal(str)
    preview = Signal(dict)

    def __init__(self, result: dict) -> None:
        super().__init__()
        self._result = result
        self._filepath = str(result.get("path", ""))
        self.setObjectName("result_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        p = Path(self._filepath) if self._filepath else None
        score = float(self._result.get("score", 0))
        source = str(self._result.get("source", "unknown")).capitalize()
        ext = p.suffix.upper().lstrip(".") if p and p.suffix else "FILE"

        # Row 1: Name + Score
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        name_lbl = QLabel(p.name if p else "Unknown")
        name_lbl.setObjectName("card_title")
        row1.addWidget(name_lbl)

        badge_lbl = QLabel(f"{source} | {ext}")
        badge_lbl.setObjectName("card_badge")
        row1.addWidget(badge_lbl)

        row1.addStretch()

        # Try to get size and date dynamically
        try:
            if p and p.exists():
                size_bytes = os.path.getsize(self._filepath)
                if size_bytes < 1024 * 1024:
                    size_str = f"{size_bytes / 1024:.1f} KB"
                else:
                    size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                
                mtime = os.path.getmtime(self._filepath)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                
                meta_lbl = QLabel(f"{size_str}  •  {date_str}")
                meta_lbl.setObjectName("dim_label")
                row1.addWidget(meta_lbl)
                
                # Cache for filtering
                self._result["_size"] = size_bytes
                self._result["_mtime"] = mtime
        except Exception:
            pass

        score_lbl = QLabel(f"{score:.0%}")
        score_lbl.setObjectName("card_score")
        row1.addWidget(score_lbl)

        layout.addLayout(row1)

        # Row 2: Path
        path_lbl = QLabel(self._filepath)
        path_lbl.setObjectName("card_path")
        path_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(path_lbl)

        # Row 3: Text snippet
        content = str(self._result.get("content", "") or self._result.get("text", ""))
        if content:
            snippet = content[:200].replace("\n", " ").strip()
            if len(content) > 200:
                snippet += "..."
            snip_lbl = QLabel(snippet)
            snip_lbl.setObjectName("card_snippet")
            snip_lbl.setWordWrap(True)
            layout.addWidget(snip_lbl)

        # Row 4: Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        for text, slot in [
            ("Open", lambda: self.open_file.emit(self._filepath)),
            ("Open Folder", lambda: self.open_folder.emit(self._filepath)),
            ("Copy Path", lambda: self.copy_path.emit(self._filepath)),
            ("Preview", lambda: self.preview.emit(self._result)),
        ]:
            btn = QPushButton(text)
            btn.setObjectName("small_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)

        btn_row.addStretch()
        layout.addLayout(btn_row)

    def mouseDoubleClickEvent(self, event):
        self.open_file.emit(self._filepath)


# ── Workspace ────────────────────────────────────────────────────

class Workspace(QWidget):
    """The central search workspace."""

    search_requested = Signal(str)
    index_requested = Signal()
    action_open_file = Signal(str)
    action_open_folder = Signal(str)
    action_copy_path = Signal(str)
    action_preview = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self._all_results = []
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Location bar ─────────────────────────────────────────
        loc_bar = QWidget()
        loc_bar.setObjectName("location_bar")
        loc_bar.setFixedHeight(36)
        lb = QHBoxLayout(loc_bar)
        lb.setContentsMargins(12, 0, 12, 0)
        lb.setSpacing(8)

        loc_icon = QLabel("\U0001F4C1")  # folder emoji as placeholder
        lb.addWidget(loc_icon)

        self._location_lbl = QLabel("No location selected — use the Explorer to pick a folder")
        self._location_lbl.setObjectName("location_text")
        lb.addWidget(self._location_lbl, stretch=1)

        self._index_btn = QPushButton("Index This Folder")
        self._index_btn.setObjectName("success_btn")
        self._index_btn.setVisible(False)
        self._index_btn.clicked.connect(self.index_requested.emit)
        lb.addWidget(self._index_btn)

        layout.addWidget(loc_bar)

        # ── Search area ──────────────────────────────────────────
        search_area = QWidget()
        search_area.setObjectName("search_area")
        sa = QHBoxLayout(search_area)
        sa.setContentsMargins(12, 10, 12, 10)
        sa.setSpacing(8)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search documents... (Ctrl+F)")
        self._search_input.setFixedHeight(36)
        self._search_input.setClearButtonEnabled(True)
        self._search_input.returnPressed.connect(self._on_search)
        sa.addWidget(self._search_input, stretch=1)

        self._search_btn = QPushButton("Search")
        self._search_btn.setObjectName("accent_btn")
        self._search_btn.setFixedHeight(36)
        self._search_btn.setFixedWidth(100)
        self._search_btn.clicked.connect(self._on_search)
        sa.addWidget(self._search_btn)

        layout.addWidget(search_area)

        # ── Filters bar ──────────────────────────────────────────
        filters_bar = QWidget()
        fl = QHBoxLayout(filters_bar)
        fl.setContentsMargins(12, 0, 12, 10)
        fl.setSpacing(10)
        
        lbl = QLabel("Filters:")
        lbl.setObjectName("field_label")
        fl.addWidget(lbl)
        
        self._filter_name = QLineEdit()
        self._filter_name.setPlaceholderText("Filter by name...")
        self._filter_name.setFixedHeight(26)
        self._filter_name.textChanged.connect(self._apply_filters)
        fl.addWidget(self._filter_name, stretch=1)
        
        self._filter_type = QComboBox()
        self._filter_type.addItems(["All Types", "PDF", "Word", "Excel", "PowerPoint", "Text"])
        self._filter_type.currentIndexChanged.connect(self._apply_filters)
        fl.addWidget(self._filter_type)
        
        self._filter_size = QComboBox()
        self._filter_size.addItems(["Any Size", "< 1 MB", "1 MB - 10 MB", "> 10 MB"])
        self._filter_size.currentIndexChanged.connect(self._apply_filters)
        fl.addWidget(self._filter_size)
        
        self._filter_date = QComboBox()
        self._filter_date.addItems(["Any Time", "Today", "Last 7 Days", "Last 30 Days", "Last Year"])
        self._filter_date.currentIndexChanged.connect(self._apply_filters)
        fl.addWidget(self._filter_date)
        
        layout.addWidget(filters_bar)

        # ── Insights / count row ─────────────────────────────────
        self._insights_lbl = QLabel("")
        self._insights_lbl.setObjectName("insight_text")
        self._insights_lbl.setContentsMargins(12, 0, 12, 6)
        layout.addWidget(self._insights_lbl)

        # ── Empty state ──────────────────────────────────────────
        self._empty_state = QLabel("Select a folder and run Index to begin searching.")
        self._empty_state.setObjectName("empty_state")
        self._empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_state.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self._empty_state)

        # ── Scroll area for result cards ─────────────────────────
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVisible(False)

        self._results_container = QWidget()
        self._results_layout = QVBoxLayout(self._results_container)
        self._results_layout.setContentsMargins(10, 6, 10, 10)
        self._results_layout.setSpacing(8)
        self._results_layout.addStretch()

        self._scroll.setWidget(self._results_container)
        layout.addWidget(self._scroll, stretch=1)

    # ── Public API ───────────────────────────────────────────────

    def set_location(self, path: str) -> None:
        self._location_lbl.setText(path)
        self._index_btn.setVisible(True)

    def focus_search(self) -> None:
        self._search_input.setFocus()
        self._search_input.selectAll()

    def set_busy(self, busy: bool) -> None:
        self._search_btn.setEnabled(not busy)
        self._search_input.setEnabled(not busy)

    def set_results(self, results: list[dict]) -> None:
        self._all_results = results
        
        # Reset filters when new search arrives
        self._filter_name.blockSignals(True)
        self._filter_type.blockSignals(True)
        self._filter_size.blockSignals(True)
        self._filter_date.blockSignals(True)
        
        self._filter_name.clear()
        self._filter_type.setCurrentIndex(0)
        self._filter_size.setCurrentIndex(0)
        self._filter_date.setCurrentIndex(0)
        
        self._filter_name.blockSignals(False)
        self._filter_type.blockSignals(False)
        self._filter_size.blockSignals(False)
        self._filter_date.blockSignals(False)
        
        self._render_results(self._all_results)

    def _render_results(self, results: list[dict]) -> None:
        # Clear old cards
        while self._results_layout.count() > 1:
            item = self._results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not results:
            self._empty_state.setText("No results found.")
            self._empty_state.setVisible(True)
            self._scroll.setVisible(False)
            self._insights_lbl.setText(f"Found 0 results (out of {len(self._all_results)})")
            return

        self._empty_state.setVisible(False)
        self._scroll.setVisible(True)

        # Insights
        exact = sum(1 for r in results if r.get("source") == "exact")
        fuzzy = sum(1 for r in results if r.get("source") == "fuzzy")
        semantic = sum(1 for r in results if r.get("source") == "semantic")
        total = len(results)
        
        msg = f"Showing {total} results"
        if len(self._all_results) != total:
            msg += f" (filtered from {len(self._all_results)})"
        msg += f"   |   Exact: {exact}   Fuzzy: {fuzzy}   Semantic: {semantic}"
            
        self._insights_lbl.setText(msg)

        # Insert new cards before the stretch
        for r in results:
            card = _ResultCard(r)
            card.open_file.connect(self.action_open_file.emit)
            card.open_folder.connect(self.action_open_folder.emit)
            card.copy_path.connect(self.action_copy_path.emit)
            card.preview.connect(self.action_preview.emit)
            self._results_layout.insertWidget(self._results_layout.count() - 1, card)

    # ── Private ──────────────────────────────────────────────────
    
    def _apply_filters(self) -> None:
        name_q = self._filter_name.text().lower().strip()
        type_idx = self._filter_type.currentIndex()
        size_idx = self._filter_size.currentIndex()
        date_idx = self._filter_date.currentIndex()
        
        now = time.time()
        
        filtered = []
        for r in self._all_results:
            path_str = str(r.get("path", ""))
            p = Path(path_str)
            
            # 1. Name filter
            if name_q and name_q not in p.name.lower():
                continue
                
            # 2. Type filter
            ext = p.suffix.lower()
            if type_idx == 1 and ext != ".pdf": continue
            if type_idx == 2 and ext not in (".doc", ".docx"): continue
            if type_idx == 3 and ext not in (".xls", ".xlsx"): continue
            if type_idx == 4 and ext not in (".ppt", ".pptx"): continue
            if type_idx == 5 and ext != ".txt": continue
            
            # Pre-fetch stats if not cached
            if "_size" not in r or "_mtime" not in r:
                try:
                    r["_size"] = os.path.getsize(path_str)
                    r["_mtime"] = os.path.getmtime(path_str)
                except Exception:
                    r["_size"] = 0
                    r["_mtime"] = 0
                    
            size = r.get("_size", 0)
            mtime = r.get("_mtime", 0)
            
            # 3. Size filter
            mb = 1024 * 1024
            if size_idx == 1 and size >= 1 * mb: continue
            if size_idx == 2 and (size < 1 * mb or size > 10 * mb): continue
            if size_idx == 3 and size <= 10 * mb: continue
            
            # 4. Date filter
            days_diff = (now - mtime) / (60 * 60 * 24)
            if date_idx == 1 and days_diff > 1: continue
            if date_idx == 2 and days_diff > 7: continue
            if date_idx == 3 and days_diff > 30: continue
            if date_idx == 4 and days_diff > 365: continue
            
            filtered.append(r)
            
        self._render_results(filtered)

    def _on_search(self) -> None:
        query = self._search_input.text().strip()
        if query:
            state.add_search_history(query)
            self._insights_lbl.setText("Searching...")
            self.search_requested.emit(query)
