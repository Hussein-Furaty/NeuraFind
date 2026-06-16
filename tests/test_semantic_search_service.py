from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import (
    SentenceTransformerModel,
)
from src.neurafind.search.semantic_search_service import SemanticSearchService


def main():
    model = SentenceTransformerModel()
    embedding_service = EmbeddingService(model)

    service = SemanticSearchService(
        database_path="neurafind_test.db",
        embedding_service=embedding_service,
    )

    query = input("Semantic search query: ")

    results = service.search(query)

    print(f"\nFound {len(results)} documents\n")

    for document in results[:5]:
        print("=" * 80)
        print(f"Score: {document['score']:.4f}")
        print(document["path"])


if __name__ == "__main__":
    main()