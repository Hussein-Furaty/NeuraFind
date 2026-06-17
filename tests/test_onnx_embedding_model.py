from src.neurafind.embeddings.models.onnx_embedding_model import ONNXEmbeddingModel


def main():
    model = ONNXEmbeddingModel("models/minilm-onnx")

    text = "الأمن السيبراني وحماية الشبكات"
    embedding = model.embed(text)

    print("Text:", text)
    print("Embedding size:", len(embedding))
    print(embedding[:10])


if __name__ == "__main__":
    main()