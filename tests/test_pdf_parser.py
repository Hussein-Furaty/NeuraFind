from src.neurafind.parsers.pdf_parser import PdfParser


def main():
    parser = PdfParser()

    pdf_path = input("PDF path: ")

    text = parser.extract_text(pdf_path)

    print("\n--- Extracted Text ---\n")
    print(text[:2000])


if __name__ == "__main__":
    main()
