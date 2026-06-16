"""Toast notification system."""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


class ToastNotification(QWidget):
    """A floating toast that auto-dismisses."""

    def __init__(self, parent, message: str, type_: str = "info", duration_ms: int = 3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build(message, type_)
        self._duration = duration_ms
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.close)

    def _build(self, message: str, type_: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setObjectName("toast_frame")
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(16, 10, 16, 10)

        lbl = QLabel(message)
        lbl.setWordWrap(True)
        fl.addWidget(lbl)

        layout.addWidget(frame)
        self.setFixedWidth(360)
        self.adjustSize()

    def show_toast(self) -> None:
        if self.parent():
            pr = self.parent().geometry()
            x = pr.x() + pr.width() - self.width() - 20
            y = pr.y() + pr.height() - self.height() - 50
            self.move(x, y)
        self.show()
        self.raise_()
        self._timer.start(self._duration)
