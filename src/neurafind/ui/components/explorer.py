"""File Explorer component (Left Sidebar)."""

from pathlib import Path

from PySide6.QtCore import Qt, Signal, QDir
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTreeWidget, QTreeWidgetItem, QStyle,
)


class FileExplorer(QWidget):
    """Tree-based file explorer similar to VS Code / PyCharm."""

    location_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("explorer_header")
        header.setFixedHeight(30)
        hlayout = QHBoxLayout(header)
        hlayout.setContentsMargins(12, 0, 8, 0)
        title = QLabel("EXPLORER")
        title.setObjectName("panel_title")
        hlayout.addWidget(title)
        hlayout.addStretch()
        layout.addWidget(header)

        # Tree
        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setRootIsDecorated(True)
        self._tree.setAnimated(False)
        self._tree.setIndentation(16)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemExpanded.connect(self._on_item_expanded)
        layout.addWidget(self._tree)

        self._populate_initial()

    def _populate_initial(self) -> None:
        dir_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        drive_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DriveHDIcon)

        # Quick Access
        qa = QTreeWidgetItem(self._tree, ["Quick Access"])
        qa.setFlags(qa.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        f = qa.font(0)
        f.setBold(True)
        qa.setFont(0, f)
        qa.setExpanded(True)

        home = Path.home()
        for name, folder in [
            ("Desktop", home / "Desktop"),
            ("Documents", home / "Documents"),
            ("Downloads", home / "Downloads"),
        ]:
            if folder.exists():
                item = QTreeWidgetItem(qa, [name])
                item.setData(0, Qt.ItemDataRole.UserRole, str(folder))
                item.setIcon(0, dir_icon)
                ph = QTreeWidgetItem(item)
                ph.setData(0, Qt.ItemDataRole.UserRole, "__ph__")

        # This PC
        pc = QTreeWidgetItem(self._tree, ["This PC"])
        pc.setFlags(pc.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        f2 = pc.font(0)
        f2.setBold(True)
        pc.setFont(0, f2)
        pc.setExpanded(True)

        for drive_info in QDir.drives():
            drive_path = drive_info.absoluteFilePath()
            item = QTreeWidgetItem(pc, [drive_path])
            item.setData(0, Qt.ItemDataRole.UserRole, drive_path)
            item.setIcon(0, drive_icon)
            ph = QTreeWidgetItem(item)
            ph.setData(0, Qt.ItemDataRole.UserRole, "__ph__")

    def _on_item_clicked(self, item: QTreeWidgetItem, _col: int) -> None:
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and path != "__ph__":
            self.location_selected.emit(path)

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        if item.childCount() == 1:
            child = item.child(0)
            if child and child.data(0, Qt.ItemDataRole.UserRole) == "__ph__":
                item.removeChild(child)
                folder_path = item.data(0, Qt.ItemDataRole.UserRole)
                if folder_path:
                    self._populate_folder(item, folder_path)

    def _populate_folder(self, parent: QTreeWidgetItem, folder_path: str) -> None:
        dir_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        try:
            p = Path(folder_path)
            subfolders = sorted(
                [
                    f for f in p.iterdir()
                    if f.is_dir()
                    and not f.name.startswith(".")
                    and not f.name.startswith("$")
                ],
                key=lambda x: x.name.lower(),
            )
            for folder in subfolders[:300]:
                item = QTreeWidgetItem(parent, [folder.name])
                item.setData(0, Qt.ItemDataRole.UserRole, str(folder))
                item.setIcon(0, dir_icon)
                ph = QTreeWidgetItem(item)
                ph.setData(0, Qt.ItemDataRole.UserRole, "__ph__")
        except (PermissionError, OSError):
            pass
