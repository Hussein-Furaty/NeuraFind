from pathlib import Path

from src.neurafind.parsers.docx_parser import DocxParser
from src.neurafind.parsers.pdf_parser import PdfParser
from src.neurafind.parsers.pptx_parser import PptxParser
from src.neurafind.parsers.xlsx_parser import XlsxParser


class ParserManager:
    """Selects the appropriate parser for supported document files."""

    def __init__(self):
        self.parsers = {
            ".pdf": PdfParser(),
            ".docx": DocxParser(),
            ".xlsx": XlsxParser(),
            ".pptx": PptxParser(),
        }

    def extract_text(self, file_path: str | Path) -> str:
        path = Path(file_path)
        parser = self.parsers.get(path.suffix.lower())

        if parser is None:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        return parser.extract_text(path)