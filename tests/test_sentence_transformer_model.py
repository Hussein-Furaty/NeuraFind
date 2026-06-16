from src.neurafind.embeddings.embedding_service import EmbeddingService
from src.neurafind.embeddings.models.sentence_transformer_model import SentenceTransformerModel


def main():
    model = SentenceTransformerModel()
    service = EmbeddingService(model)

    text = input("Text: ")

    embedding = service.embed_text(text)

    print(f"Embedding size: {len(embedding)}")
    print(embedding[:10])


if __name__ == "__main__":
    main()