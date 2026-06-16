from src.neurafind.search.fuzzy_search_service import FuzzySearchService


def main():
    service = FuzzySearchService("neurafind_test.db")

    query = input("Fuzzy search query: ")

    results = service.search(query)

    print(f"\nFound {len(results)} matching documents\n")

    for document in results:
        print("=" * 80)
        print(f"Score: {document['score']}")
        print(document["path"])


if __name__ == "__main__":
    main()