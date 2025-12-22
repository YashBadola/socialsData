import re
import sys
import argparse
from pathlib import Path

def clean_text(text):
    """
    Strips Project Gutenberg headers and footers from text.
    """
    # Gutenberg header/footer markers are somewhat inconsistent, but usually follow this pattern.

    # Try to find the start
    start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    if start_match:
        text = text[start_match.end():]

    # Try to find the end
    end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    if end_match:
        text = text[:end_match.start()]

    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Clean Gutenberg text files.")
    parser.add_argument("filepath", type=str, help="Path to the file to clean")
    args = parser.parse_args()

    file_path = Path(args.filepath)
    if not file_path.exists():
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    try:
        content = file_path.read_text(encoding="utf-8")
        cleaned_content = clean_text(content)

        # Overwrite the file
        file_path.write_text(cleaned_content, encoding="utf-8")
        print(f"Successfully cleaned {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
