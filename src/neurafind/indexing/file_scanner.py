from pathlib import Path


class FileScanner:
    """Scans directories for supported document files."""

    def scan_pdfs(self, folder_path: str) -> list[Path]:
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")

        if not folder.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {folder_path}")

        return list(folder.rglob("*.pdf"))
