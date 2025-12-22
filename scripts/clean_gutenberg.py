import re
import sys

def clean_text(text):
    # Remove Gutenberg header
    # Different patterns might be needed, this is a common one
    # "START OF THE PROJECT GUTENBERG EBOOK" or similar
    start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if start_match:
        text = text[start_match.end():]

    # Remove Gutenberg footer
    end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
    if end_match:
        text = text[:end_match.start()]

    return text.strip()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_gutenberg.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = clean_text(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
