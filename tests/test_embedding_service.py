from src.neurafind.embeddings.embedding_model import EmbeddingModel
from src.neurafind.embeddings.embedding_service import EmbeddingService


class DummyEmbeddingModel(EmbeddingModel):
    def embed(self, text: str) -> list[float]:
        return [float(len(text)), 1.0]


def main():
    service = EmbeddingService(DummyEmbeddingModel())

    text = input("Text: ")

    embedding = service.embed_text(text)

    print(embedding)


if __name__ == "__main__":
    main()