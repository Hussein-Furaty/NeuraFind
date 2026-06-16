from pathlib import Path

from docx import Document


class DocxParser:
    """Extracts text content from DOCX documents."""

    def extract_text(self, file_path: str | Path) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document does not exist: {path}")

        if path.suffix.lower() != ".docx":
            raise ValueError(f"Unsupported file type: {path.suffix}")

        document = Document(path)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)