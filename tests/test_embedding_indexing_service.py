from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import (
    SentenceTransformerModel,
)
from src.neurafind.services.embedding_indexing_service import (
    EmbeddingIndexingService,
)


def main():
    model = SentenceTransformerModel()
    embedding_service = EmbeddingService(model)

    service = EmbeddingIndexingService(
        database_path="neurafind_test.db",
        embedding_service=embedding_service,
    )

    folder_path = input("Folder path: ")

    count = service.index_folder(folder_path)

    print(f"Indexed {count} documents with embeddings.")


if __name__ == "__main__":
    main()