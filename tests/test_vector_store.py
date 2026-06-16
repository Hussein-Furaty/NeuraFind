from src.neurafind.storage.vector_store import VectorStore


def main():
    store = VectorStore("neurafind_test.db")

    store.save_embedding(
        "sample.pdf",
        [0.1, 0.2, 0.3],
    )

    embedding = store.get_embedding(
        "sample.pdf",
    )

    print(embedding)


if __name__ == "__main__":
    main()