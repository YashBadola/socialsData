import sys
import re

def clean_gutenberg(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start of the book (flexible patterns)
    # The pattern should match lines like "*** START OF THE PROJECT GUTENBERG EBOOK, TITLE ***"
    # or "*** START OF THIS PROJECT GUTENBERG EBOOK TITLE ***"
    start_pattern = r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.* \*\*\*"
    match_start = re.search(start_pattern, text)
    if match_start:
        text = text[match_start.end():]
        print(f"Found start marker.")
    else:
        print("Warning: Start marker not found.")

    # Find the end of the book
    end_pattern = r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.* \*\*\*"
    match_end = re.search(end_pattern, text)
    if match_end:
        text = text[:match_end.start()]
        print(f"Found end marker.")
    else:
        print("Warning: End marker not found.")

    # Strip extra whitespace
    text = text.strip()

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean_gutenberg.py <filepath>")
        sys.exit(1)

    clean_gutenberg(sys.argv[1])
