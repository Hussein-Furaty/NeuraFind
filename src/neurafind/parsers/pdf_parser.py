from pathlib import Path

import fitz


class PdfParser:
    """Extracts text content from PDF documents."""

    def extract_text(self, file_path: str | Path) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF file does not exist: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Unsupported file type: {path.suffix}")

        text_parts: list[str] = []

        with fitz.open(path) as document:
            for page in document:
                text_parts.append(page.get_text())

        return "\n".join(text_parts).strip()