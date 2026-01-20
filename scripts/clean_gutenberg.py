import sys
import re

def clean_gutenberg(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start of the book (flexible patterns)
    start_patterns = [
        r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*",
        r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK", # simplified
    ]

    start_pos = 0
    for pattern in start_patterns:
        match_start = re.search(pattern, text, re.IGNORECASE)
        if match_start:
            # We want the last occurrence if there are multiple (headers sometimes repeat?)
            # No, usually the first one.
            # But we want to cut everything BEFORE this.
            start_pos = match_start.end()
            break

    if start_pos > 0:
        text = text[start_pos:]

    # Find the end of the book
    end_patterns = [
        r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*",
        r"End of the Project Gutenberg EBook",
        r"End of Project Gutenberg's",
    ]

    end_pos = None
    for pattern in end_patterns:
        match_end = re.search(pattern, text, re.IGNORECASE)
        if match_end:
            # We want to cut everything AFTER this.
            end_pos = match_end.start()
            break

    if end_pos is not None:
        text = text[:end_pos]

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
