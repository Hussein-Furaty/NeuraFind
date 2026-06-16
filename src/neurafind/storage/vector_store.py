import json
import sqlite3
from pathlib import Path


class VectorStore:
    """Stores document embeddings in SQLite."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self._initialize_database()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize_database(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    document_path TEXT PRIMARY KEY,
                    embedding TEXT NOT NULL
                )
                """
            )

    def save_embedding(
        self,
        document_path: str,
        embedding: list[float],
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO embeddings
                (document_path, embedding)
                VALUES (?, ?)
                """,
                (
                    document_path,
                    json.dumps(embedding),
                ),
            )

    def get_embedding(
        self,
        document_path: str,
    ) -> list[float] | None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT embedding
                FROM embeddings
                WHERE document_path = ?
                """,
                (document_path,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return json.loads(row[0])