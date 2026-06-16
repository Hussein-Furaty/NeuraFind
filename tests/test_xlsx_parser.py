from src.neurafind.parsers.xlsx_parser import XlsxParser


def main():
    parser = XlsxParser()

    xlsx_path = input("XLSX path: ")

    text = parser.extract_text(xlsx_path)

    print("\n--- Extracted Text ---\n")
    print(text[:2000])


if __name__ == "__main__":
    main()