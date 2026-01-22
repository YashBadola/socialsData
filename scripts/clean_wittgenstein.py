import sys
import re

def clean_wittgenstein(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start of the book
    start_pattern = r"\*\*\* START OF .*PROJECT GUTENBERG EBOOK.* \*\*\*"
    match_start = re.search(start_pattern, text)
    if match_start:
        text = text[match_start.end():]
    else:
        print("Warning: Start marker not found!")

    # Find the end of the book
    end_pattern = r"\*\*\* END OF .*PROJECT GUTENBERG EBOOK.* \*\*\*"
    match_end = re.search(end_pattern, text)
    if match_end:
        text = text[:match_end.start()]
    else:
        print("Warning: End marker not found!")

    # Strip extra whitespace
    text = text.strip()

    # Save back
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cleaned {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/clean_wittgenstein.py <input_path> <output_path>")
        sys.exit(1)

    clean_wittgenstein(sys.argv[1], sys.argv[2])
