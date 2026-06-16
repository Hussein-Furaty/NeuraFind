from src.neurafind.search.search_service import SearchService


def main():
    service = SearchService("neurafind_test.db")

    query = input("Search query: ")

    results = service.search(query)

    print(f"\nFound {len(results)} matching documents\n")

    for document in results:
        print("=" * 80)
        print(document["path"])


if __name__ == "__main__":
    main()