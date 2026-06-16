from pathlib import Path


class FileScanner:
    """Scans directories for supported document files."""

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".xlsx",
        ".pptx",
    }

    def scan(self, folder_path: str) -> list[Path]:
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")

        if not folder.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {folder_path}")

        files: list[Path] = []

        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                files.append(file_path)

        return files