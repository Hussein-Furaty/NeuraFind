"""Professional IDE-style Application Splash Screen."""

from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPixmap, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QFrame
)


def _logo_path() -> str:
    return str(
        Path(__file__).resolve().parent.parent.parent.parent
        / "assets"
        / "NeuraFind.png"
    )


class NeonSpinner(QWidget):
    """A custom widget that draws a spinning neon circle."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._rotate)
        self.timer.start(20)
        
    def _rotate(self):
        self.angle = (self.angle + 8) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(10, 10, 40, 40)
        
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.translate(-self.width() / 2, -self.height() / 2)
        
        # Base faint circle
        base_pen = QPen(QColor(59, 130, 246, 30))
        base_pen.setWidth(3)
        painter.setPen(base_pen)
        painter.drawEllipse(rect)
        
        span_angle = 140 * 16
        
        # Glow 1 (Outer, wide, transparent)
        pen1 = QPen(QColor(59, 130, 246, 50))
        pen1.setWidth(9)
        pen1.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen1)
        painter.drawArc(rect, 0, span_angle)
        
        # Glow 2 (Middle)
        pen2 = QPen(QColor(59, 130, 246, 120))
        pen2.setWidth(5)
        pen2.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen2)
        painter.drawArc(rect, 0, span_angle)
        
        # Core (Inner, solid bright white/blue)
        pen3 = QPen(QColor(219, 234, 254, 255))
        pen3.setWidth(2)
        pen3.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen3)
        painter.drawArc(rect, 0, span_angle)


class SplashScreen(QWidget):
    """Custom frameless splash screen with progress info."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(480, 460)
        self._build()
        
        self._tick = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_text)
        self._timer.start(500)

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 12px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(30, 30, 30, 24)
        fl.setSpacing(0)
        
        # ── Logo ──
        import os
        logo = _logo_path()
        logo_lbl = QLabel()
        logo_lbl.setFixedSize(160, 160)
        if os.path.exists(logo):
            pm = QPixmap(logo).scaled(
                160, 160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl.setPixmap(pm)
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Center the logo horizontally
        logo_row = QHBoxLayout()
        logo_row.addStretch()
        logo_row.addWidget(logo_lbl)
        logo_row.addStretch()
        fl.addLayout(logo_row)
        
        fl.addSpacing(12)
        
        # ── Title ──
        title = QLabel("NeuraFind")
        title.setStyleSheet("color: #ffffff; font-size: 30px; font-weight: bold; font-family: 'Segoe UI';")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFixedHeight(40)
        fl.addWidget(title)
        
        # ── Subtitle ──
        sub = QLabel("Document Intelligence Platform")
        sub.setStyleSheet("color: #94a3b8; font-size: 13px; font-family: 'Segoe UI'; letter-spacing: 1px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setFixedHeight(22)
        fl.addWidget(sub)
        
        fl.addSpacing(16)
        
        # ── Neon spinner ──
        self.spinner = NeonSpinner()
        spinner_layout = QHBoxLayout()
        spinner_layout.addStretch()
        spinner_layout.addWidget(self.spinner)
        spinner_layout.addStretch()
        fl.addLayout(spinner_layout)
        
        fl.addStretch()
        
        # ── Bottom area ──
        bottom_layout = QHBoxLayout()
        
        ver = QLabel("Version 1.0.0")
        ver.setStyleSheet("color: #475569; font-size: 11px; font-weight: bold;")
        bottom_layout.addWidget(ver)
        
        bottom_layout.addStretch()
        
        self.loading_text = QLabel("Initializing core services...")
        self.loading_text.setStyleSheet("color: #64748b; font-size: 11px; font-style: italic;")
        bottom_layout.addWidget(self.loading_text)
        
        fl.addLayout(bottom_layout)
        layout.addWidget(frame)

    def _update_text(self):
        self._tick += 1
        if self._tick == 2:
            self.loading_text.setText("Loading AI embedding models...")
        elif self._tick == 4:
            self.loading_text.setText("Connecting to vector database...")
        elif self._tick == 6:
            self.loading_text.setText("Preparing workspace...")

    def finish(self, main_window):
        self._timer.stop()
        self.spinner.timer.stop()
        self.loading_text.setText("Ready.")
        QApplication.processEvents()
        self.close()


def show_splash():
    """Create and display the splash screen."""
    splash = SplashScreen()
    splash.show()
    QApplication.processEvents()
    return splash