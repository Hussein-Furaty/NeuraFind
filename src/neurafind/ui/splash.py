"""Application splash screen."""

import os
from pathlib import Path
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QSplashScreen, QApplication

def _logo_path() -> str:
    return str(Path(__file__).resolve().parent.parent.parent.parent / "assets" / "neurafind-logo.png")

def show_splash():
    """Create and display the splash screen."""
    logo = _logo_path()
    
    # We create a pixmap and manually draw the text to make it professional
    if os.path.exists(logo):
        pixmap = QPixmap(logo).scaled(
            400, 400,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    else:
        # Fallback empty splash
        pixmap = QPixmap(400, 300)
        pixmap.fill(QColor("#1e1e1e"))

    splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    
    # Process events so it draws immediately
    QApplication.processEvents()
    
    return splash
