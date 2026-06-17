import sqlite3
from pathlib import Path


class DocumentStore:
    """Stores indexed document content and metadata in SQLite."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL UNIQUE,
                    file_type TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )

    def save_documents(self, documents: list[dict[str, str]]) -> None:
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT OR REPLACE INTO documents (path, file_type, content)
                VALUES (:path, :file_type, :content)
                """,
                [
                    document
                    for document in documents
                    if document.get("content") and "error" not in document
                ],
            )

    def get_all_documents(self, location_filter: str = None) -> list[dict[str, str]]:
        with self._connect() as connection:
            if location_filter:
                import os
                filter_path = os.path.normpath(location_filter).lower()
                cursor = connection.execute(
                    """
                    SELECT path, file_type, content
                    FROM documents
                    WHERE LOWER(path) LIKE ?
                    ORDER BY path
                    """,
                    (f"{filter_path}%",),
                )
            else:
                cursor = connection.execute(
                    """
                    SELECT path, file_type, content
                    FROM documents
                    ORDER BY path
                    """
                )

            return [
                {
                    "path": row[0],
                    "file_type": row[1],
                    "content": row[2],
                }
                for row in cursor.fetchall()
            ]