from src.neurafind.parsers.parser_manager import ParserManager


def main():
    manager = ParserManager()

    file_path = input("Document path: ")

    text = manager.extract_text(file_path)

    print("\n--- Extracted Text ---\n")
    print(text[:2000])


if __name__ == "__main__":
    main()