from pathlib import Path

from src.neurafind.indexing.file_scanner import FileScanner
from src.neurafind.parsers.parser_manager import ParserManager


class Indexer:
    """Builds a text index from supported documents inside a folder."""

    def __init__(self):
        self.scanner = FileScanner()
        self.parser_manager = ParserManager()

    def index_folder(self, folder_path: str | Path) -> list[dict[str, str]]:
        files = self.scanner.scan(str(folder_path))
        indexed_documents: list[dict[str, str]] = []

        for file_path in files:
            try:
                content = self.parser_manager.extract_text(file_path)

                indexed_documents.append(
                    {
                        "path": str(file_path),
                        "file_type": file_path.suffix.lower(),
                        "content": content,
                    }
                )

            except Exception as error:
                indexed_documents.append(
                    {
                        "path": str(file_path),
                        "file_type": file_path.suffix.lower(),
                        "content": "",
                        "error": str(error),
                    }
                )

        return indexed_documents