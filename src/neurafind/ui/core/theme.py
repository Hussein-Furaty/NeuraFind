"""Theme definitions and comprehensive stylesheet generation.

All colors are self-contained. Components must NOT use palette() or
inline setStyleSheet() with hardcoded colors. Instead, use objectName
selectors defined here so that theme switches propagate automatically.
"""

_THEMES = {
    "dark": {
        "name": "Dark",
        # Backgrounds
        "bg":              "#1e1e1e",
        "surface":         "#252526",
        "panel":           "#2d2d30",
        "sidebar":         "#252526",
        "sidebar_header":  "#333333",
        "card_bg":         "#2d2d30",
        "card_hover":      "#37373d",
        "card_selected":   "#264f78",
        # Borders
        "border":          "#3c3c3c",
        "border_light":    "#4a4a4a",
        # Text
        "text":            "#cccccc",
        "text_sec":        "#858585",
        "text_dim":        "#5a5a5a",
        # Accent
        "accent":          "#0078d4",
        "accent_hover":    "#1a8ae8",
        "accent_press":    "#005a9e",
        "accent_text":     "#ffffff",
        "accent_muted":    "rgba(0,120,212,0.15)",
        # Selection
        "selection":       "#264f78",
        "hover":           "#2a2d2e",
        # Inputs
        "input_bg":        "#3c3c3c",
        "input_border":    "#555555",
        "input_focus":     "#0078d4",
        # Buttons
        "btn_bg":          "#3c3c3c",
        "btn_border":      "#555555",
        "btn_hover":       "#4a4a4a",
        "btn_text":        "#cccccc",
        # Table
        "table_header":    "#2d2d30",
        "table_alt":       "#252526",
        "table_grid":      "#3c3c3c",
        # Toolbar
        "toolbar_bg":      "#2d2d30",
        "toolbar_border":  "#3c3c3c",
        "toolbar_hover":   "#3e3e3e",
        # Status bar
        "statusbar_bg":    "#007acc",
        "statusbar_text":  "#ffffff",
        # Scrollbar
        "scroll_handle":   "#424242",
        "scroll_hover":    "#555555",
        # Semantic colors
        "success":         "#4ec9b0",
        "error":           "#f44747",
        "warning":         "#cca700",
        "info":            "#3794ff",
        # Toast
        "toast_bg":        "#333333",
        "toast_border":    "#555555",
        # Search
        "search_bg":       "#3c3c3c",
    },
    "light": {
        "name": "Light",
        "bg":              "#f0f0f0",
        "surface":         "#ffffff",
        "panel":           "#f5f5f5",
        "sidebar":         "#f3f3f3",
        "sidebar_header":  "#e8e8e8",
        "card_bg":         "#ffffff",
        "card_hover":      "#e8f0fe",
        "card_selected":   "#cce5ff",
        "border":          "#d4d4d4",
        "border_light":    "#e0e0e0",
        "text":            "#1e1e1e",
        "text_sec":        "#616161",
        "text_dim":        "#999999",
        "accent":          "#0078d4",
        "accent_hover":    "#1a8ae8",
        "accent_press":    "#005a9e",
        "accent_text":     "#ffffff",
        "accent_muted":    "rgba(0,120,212,0.10)",
        "selection":       "#cce5ff",
        "hover":           "#e8e8e8",
        "input_bg":        "#ffffff",
        "input_border":    "#cccccc",
        "input_focus":     "#0078d4",
        "btn_bg":          "#e4e4e4",
        "btn_border":      "#cccccc",
        "btn_hover":       "#d4d4d4",
        "btn_text":        "#1e1e1e",
        "table_header":    "#f0f0f0",
        "table_alt":       "#fafafa",
        "table_grid":      "#e0e0e0",
        "toolbar_bg":      "#e8e8e8",
        "toolbar_border":  "#d4d4d4",
        "toolbar_hover":   "#d0d0d0",
        "statusbar_bg":    "#007acc",
        "statusbar_text":  "#ffffff",
        "scroll_handle":   "#c0c0c0",
        "scroll_hover":    "#a0a0a0",
        "success":         "#16825d",
        "error":           "#cd3131",
        "warning":         "#bf8803",
        "info":            "#0078d4",
        "toast_bg":        "#ffffff",
        "toast_border":    "#d4d4d4",
        "search_bg":       "#ffffff",
    },
}


def get_theme(name: str) -> dict:
    return _THEMES.get(name, _THEMES["dark"])


def build_stylesheet(t: dict) -> str:
    """Build a complete QSS stylesheet from a theme dict.

    Every color used in the application MUST come from this stylesheet
    so that theme switches propagate correctly to all widgets.
    """
    return f"""
/* ═══════════════════════════════════════════════════════════════
   Global
   ═══════════════════════════════════════════════════════════════ */
* {{
    font-family: "Segoe UI", "Segoe UI Variable", system-ui, sans-serif;
    font-size: 13px;
    outline: none;
}}
QMainWindow {{
    background-color: {t["bg"]};
    color: {t["text"]};
}}
QWidget {{
    color: {t["text"]};
}}
QDialog {{
    background-color: {t["bg"]};
    color: {t["text"]};
}}

/* ═══════════════════════════════════════════════════════════════
   Menu Bar
   ═══════════════════════════════════════════════════════════════ */
QMenuBar {{
    background-color: {t["panel"]};
    color: {t["text"]};
    border-bottom: 1px solid {t["border"]};
    padding: 0;
}}
QMenuBar::item {{
    background: transparent;
    padding: 5px 10px;
}}
QMenuBar::item:selected {{
    background-color: {t["hover"]};
}}
QMenu {{
    background-color: {t["surface"]};
    color: {t["text"]};
    border: 1px solid {t["border"]};
    padding: 4px 0;
}}
QMenu::item {{
    padding: 6px 28px 6px 24px;
}}
QMenu::item:selected {{
    background-color: {t["accent_muted"]};
}}
QMenu::separator {{
    height: 1px;
    background: {t["border"]};
    margin: 4px 10px;
}}

/* ═══════════════════════════════════════════════════════════════
   Toolbar
   ═══════════════════════════════════════════════════════════════ */
QToolBar {{
    background-color: {t["toolbar_bg"]};
    border-bottom: 1px solid {t["toolbar_border"]};
    spacing: 2px;
    padding: 3px 6px;
}}
QToolBar::separator {{
    width: 1px;
    background: {t["border"]};
    margin: 4px 6px;
}}
QToolBar QToolButton {{
    background: transparent;
    color: {t["text"]};
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 12px;
}}
QToolBar QToolButton:hover {{
    background-color: {t["toolbar_hover"]};
}}

/* ═══════════════════════════════════════════════════════════════
   Inputs
   ═══════════════════════════════════════════════════════════════ */
QLineEdit {{
    background-color: {t["input_bg"]};
    color: {t["text"]};
    border: 1px solid {t["input_border"]};
    border-radius: 4px;
    padding: 5px 10px;
    selection-background-color: {t["accent"]};
    selection-color: {t["accent_text"]};
}}
QLineEdit:focus {{
    border: 1px solid {t["input_focus"]};
}}
QComboBox {{
    background-color: {t["input_bg"]};
    color: {t["text"]};
    border: 1px solid {t["input_border"]};
    border-radius: 4px;
    padding: 5px 10px;
    min-height: 22px;
}}
QComboBox:hover {{
    border-color: {t["accent"]};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {t["surface"]};
    color: {t["text"]};
    border: 1px solid {t["border"]};
    selection-background-color: {t["accent_muted"]};
    selection-color: {t["text"]};
}}
QSpinBox, QDoubleSpinBox {{
    background-color: {t["input_bg"]};
    color: {t["text"]};
    border: 1px solid {t["input_border"]};
    border-radius: 4px;
    padding: 4px 8px;
}}

/* ═══════════════════════════════════════════════════════════════
   Buttons
   ═══════════════════════════════════════════════════════════════ */
QPushButton {{
    background-color: {t["btn_bg"]};
    color: {t["btn_text"]};
    border: 1px solid {t["btn_border"]};
    border-radius: 4px;
    padding: 6px 16px;
    font-size: 12px;
    min-height: 24px;
}}
QPushButton:hover {{
    background-color: {t["btn_hover"]};
}}
QPushButton:disabled {{
    color: {t["text_dim"]};
}}
QPushButton#accent_btn {{
    background-color: {t["accent"]};
    color: {t["accent_text"]};
    border: none;
    font-weight: 600;
}}
QPushButton#accent_btn:hover {{
    background-color: {t["accent_hover"]};
}}
QPushButton#accent_btn:pressed {{
    background-color: {t["accent_press"]};
}}
QPushButton#accent_btn:disabled {{
    background-color: {t["btn_bg"]};
    color: {t["text_dim"]};
    border: 1px solid {t["btn_border"]};
}}
QPushButton#small_btn {{
    padding: 3px 10px;
    font-size: 11px;
    min-height: 20px;
    border-radius: 3px;
}}
QPushButton#success_btn {{
    background-color: {t["success"]};
    color: #ffffff;
    border: none;
    font-weight: 600;
}}
QPushButton#success_btn:hover {{
    opacity: 0.9;
}}

/* ═══════════════════════════════════════════════════════════════
   Tree (Explorer)
   ═══════════════════════════════════════════════════════════════ */
QTreeWidget {{
    background-color: {t["sidebar"]};
    color: {t["text"]};
    border: none;
    font-size: 13px;
}}
QTreeWidget::item {{
    padding: 3px 4px;
    border: none;
}}
QTreeWidget::item:hover {{
    background-color: {t["hover"]};
}}
QTreeWidget::item:selected {{
    background-color: {t["selection"]};
    color: {t["text"]};
}}
QTreeWidget::branch {{
    background: transparent;
}}

/* ═══════════════════════════════════════════════════════════════
   Splitter
   ═══════════════════════════════════════════════════════════════ */
QSplitter::handle {{
    background-color: {t["border"]};
}}
QSplitter::handle:horizontal {{ width: 1px; }}
QSplitter::handle:vertical {{ height: 1px; }}
QSplitter::handle:hover {{ background-color: {t["accent"]}; }}

/* ═══════════════════════════════════════════════════════════════
   Status Bar
   ═══════════════════════════════════════════════════════════════ */
QStatusBar {{
    background-color: {t["statusbar_bg"]};
    color: {t["statusbar_text"]};
    font-size: 12px;
    min-height: 22px;
    border: none;
}}
QStatusBar::item {{ border: none; }}
QStatusBar QProgressBar {{
    background-color: rgba(0,0,0,0.2);
    border: none;
    border-radius: 2px;
    max-height: 10px;
}}
QStatusBar QProgressBar::chunk {{
    background-color: rgba(255,255,255,0.65);
    border-radius: 2px;
}}

/* ═══════════════════════════════════════════════════════════════
   Progress Bar (generic)
   ═══════════════════════════════════════════════════════════════ */
QProgressBar {{
    background-color: {t["input_bg"]};
    border: none;
    border-radius: 3px;
    max-height: 6px;
    min-height: 6px;
}}
QProgressBar::chunk {{
    background-color: {t["accent"]};
    border-radius: 3px;
}}

/* ═══════════════════════════════════════════════════════════════
   Scrollbars
   ═══════════════════════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: {t["scroll_handle"]};
    border-radius: 5px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {t["scroll_hover"]}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
}}
QScrollBar::handle:horizontal {{
    background: {t["scroll_handle"]};
    border-radius: 5px;
    min-width: 20px;
}}
QScrollBar::handle:horizontal:hover {{ background: {t["scroll_hover"]}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ═══════════════════════════════════════════════════════════════
   Plain Text (preview)
   ═══════════════════════════════════════════════════════════════ */
QPlainTextEdit {{
    background-color: {t["surface"]};
    color: {t["text"]};
    border: none;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 12px;
    selection-background-color: {t["selection"]};
}}

/* ═══════════════════════════════════════════════════════════════
   List Widget (settings nav, history)
   ═══════════════════════════════════════════════════════════════ */
QListWidget {{
    background-color: {t["sidebar"]};
    border: none;
    color: {t["text"]};
    font-size: 13px;
}}
QListWidget::item {{
    padding: 10px 16px;
    border: none;
}}
QListWidget::item:hover {{
    background-color: {t["hover"]};
}}
QListWidget::item:selected {{
    background-color: {t["selection"]};
    color: {t["text"]};
}}

/* ═══════════════════════════════════════════════════════════════
   Group Box
   ═══════════════════════════════════════════════════════════════ */
QGroupBox {{
    background-color: transparent;
    border: 1px solid {t["border"]};
    border-radius: 4px;
    margin-top: 14px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    color: {t["text"]};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: {t["text_sec"]};
}}

/* ═══════════════════════════════════════════════════════════════
   Check Box
   ═══════════════════════════════════════════════════════════════ */
QCheckBox {{
    color: {t["text"]};
    spacing: 8px;
}}

/* ═══════════════════════════════════════════════════════════════
   Named Components (objectName-based)
   ═══════════════════════════════════════════════════════════════ */

/* Explorer header */
QWidget#explorer_header {{
    background-color: {t["sidebar_header"]};
    border-bottom: 1px solid {t["border"]};
}}

/* Preview header */
QWidget#preview_header {{
    background-color: {t["sidebar_header"]};
    border-top: 1px solid {t["border"]};
}}

/* Search area */
QWidget#search_area {{
    background-color: {t["surface"]};
    border-bottom: 1px solid {t["border"]};
}}

/* Location bar */
QWidget#location_bar {{
    background-color: {t["panel"]};
    border-bottom: 1px solid {t["border"]};
}}

/* Result card */
QFrame#result_card {{
    background-color: {t["card_bg"]};
    border: 1px solid {t["border"]};
    border-radius: 6px;
}}
QFrame#result_card:hover {{
    border-color: {t["accent"]};
    background-color: {t["card_hover"]};
}}

/* Panel titles */
QLabel#panel_title {{
    color: {t["text_sec"]};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}}
QLabel#location_text {{
    color: {t["text"]};
    font-size: 13px;
}}
QLabel#result_count {{
    color: {t["text_sec"]};
    font-size: 12px;
    padding: 4px 12px;
}}
QLabel#insight_text {{
    color: {t["text_sec"]};
    font-size: 12px;
}}
QLabel#card_title {{
    color: {t["text"]};
    font-size: 14px;
    font-weight: 600;
}}
QLabel#card_path {{
    color: {t["text_sec"]};
    font-size: 12px;
}}
QLabel#card_snippet {{
    color: {t["text_dim"]};
    font-size: 12px;
}}
QLabel#card_badge {{
    color: {t["accent"]};
    font-size: 11px;
    font-weight: 600;
}}
QLabel#card_score {{
    color: {t["success"]};
    font-size: 13px;
    font-weight: 700;
}}
QLabel#field_label {{
    color: {t["text_sec"]};
    font-size: 12px;
}}
QLabel#field_value {{
    color: {t["text"]};
    font-size: 13px;
}}
QLabel#heading {{
    color: {t["text"]};
    font-size: 18px;
    font-weight: 700;
}}
QLabel#subheading {{
    color: {t["text_sec"]};
    font-size: 13px;
}}
QLabel#section_title {{
    color: {t["text"]};
    font-size: 15px;
    font-weight: 600;
}}
QLabel#dim_label {{
    color: {t["text_dim"]};
    font-size: 11px;
    font-style: italic;
}}
QLabel#success_label {{
    color: {t["success"]};
    font-weight: 600;
}}
QLabel#error_label {{
    color: {t["error"]};
    font-weight: 600;
}}
QLabel#empty_state {{
    color: {t["text_dim"]};
    font-size: 16px;
}}

/* Toast notification */
QFrame#toast_frame {{
    background-color: {t["toast_bg"]};
    border: 1px solid {t["toast_border"]};
    border-radius: 6px;
}}

/* Quick search */
QWidget#quick_search_container {{
    background-color: {t["surface"]};
    border: 1px solid {t["accent"]};
    border-radius: 8px;
}}
QLineEdit#quick_search_input {{
    background-color: {t["surface"]};
    color: {t["text"]};
    border: none;
    font-size: 18px;
    padding: 12px 16px;
}}

/* Tooltip */
QToolTip {{
    background-color: {t["surface"]};
    color: {t["text"]};
    border: 1px solid {t["border"]};
    padding: 4px 8px;
    font-size: 12px;
}}

/* Nav list in settings (right border) */
QListWidget#settings_nav {{
    border-right: 1px solid {t["border"]};
}}

/* Scrollarea for results */
QScrollArea {{
    background-color: {t["bg"]};
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background-color: {t["bg"]};
}}
"""
