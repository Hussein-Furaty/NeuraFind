from src.neurafind.indexing.indexer import Indexer


def main():
    indexer = Indexer()

    folder_path = input("Folder path: ")

    documents = indexer.index_folder(folder_path)

    print(f"\nIndexed {len(documents)} documents\n")

    for document in documents:
        print("=" * 80)
        print(f"Path: {document['path']}")
        print(f"Type: {document['file_type']}")

        if "error" in document:
            print(f"Error: {document['error']}")
        else:
            print(f"Content Length: {len(document['content'])}")


if __name__ == "__main__":
    main()