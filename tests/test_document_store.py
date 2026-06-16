from src.neurafind.storage.document_store import DocumentStore


def main():
    store = DocumentStore("neurafind_test.db")

    documents = [
        {
            "path": "sample.pdf",
            "file_type": ".pdf",
            "content": "This is a sample document.",
        }
    ]

    store.save_documents(documents)

    saved_documents = store.get_all_documents()

    print(saved_documents)


if __name__ == "__main__":
    main()