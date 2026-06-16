from src.neurafind.services.indexing_service import IndexingService


def main():
    service = IndexingService("neurafind_test.db")

    folder_path = input("Folder path: ")

    indexed_count = service.index_folder(folder_path)

    print(f"Indexed and stored {indexed_count} documents.")


if __name__ == "__main__":
    main()