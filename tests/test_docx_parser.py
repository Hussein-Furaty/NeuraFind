from src.neurafind.parsers.docx_parser import DocxParser


def main():
    parser = DocxParser()

    docx_path = input("DOCX path: ")

    text = parser.extract_text(docx_path)

    print("\n--- Extracted Text ---\n")
    print(text[:2000])


if __name__ == "__main__":
    main()
