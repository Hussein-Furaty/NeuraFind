from src.neurafind.parsers.pptx_parser import PptxParser


def main():
    parser = PptxParser()

    pptx_path = input("PPTX path: ")

    text = parser.extract_text(pptx_path)

    print("\n--- Extracted Text ---\n")
    print(text[:2000])


if __name__ == "__main__":
    main()