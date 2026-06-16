from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import (
    SentenceTransformerModel,
)
from src.neurafind.search.hybrid_search_service import HybridSearchService


def main():
    model = SentenceTransformerModel()
    embedding_service = EmbeddingService(model)

    service = HybridSearchService(
        database_path="neurafind_test.db",
        embedding_service=embedding_service,
    )

    query = input("Hybrid search query: ")

    results = service.search(query)

    print(f"\nFound {len(results)} documents\n")

    for document in results:
        print("=" * 80)
        print(f"Score: {document['score']:.4f}")
        print(f"Source: {document['source']}")
        print(document["path"])


if __name__ == "__main__":
    main()