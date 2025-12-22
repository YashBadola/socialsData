import re
import sys

def clean_gutenberg_text(text):
    # Markers for start and end of Project Gutenberg texts
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THIS PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THIS PROJECT GUTENBERG EBOOK",
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

    # If no standard markers found, look for license block at end
    if end_pos == len(text):
        license_match = re.search(r"End of the Project Gutenberg EBook", text, re.IGNORECASE)
        if license_match:
             end_pos = license_match.start()

    clean_text = text[start_pos:end_pos].strip()

    # Remove metadata/header junk that sometimes appears after start marker
    # e.g. "Produced by ..."
    lines = clean_text.split('\n')

    # Heuristic: skip lines until we see a substantial paragraph or title
    # For now, just removing empty lines from start/end

    return clean_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = clean_gutenberg_text(content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"Cleaned {file_path}")
