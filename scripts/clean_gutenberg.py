import sys
import re
import os

def clean_gutenberg_text(text):
    # Common start markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    # Common end markers
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_pos = 0
    end_pos = len(text)

    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            start_pos = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            end_pos = match.start()
            break

    return text[start_pos:end_pos].strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <file_path> [file_path ...]")
        sys.exit(1)

    for file_path in sys.argv[1:]:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        print(f"Cleaning {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned = clean_gutenberg_text(content)

            # Simple check to see if we actually removed something or if the file was already clean/unmatched
            if len(cleaned) == len(content):
                print(f"Warning: No Gutenberg markers found in {file_path}")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            print(f"Cleaned {file_path} (length: {len(content)} -> {len(cleaned)})")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
