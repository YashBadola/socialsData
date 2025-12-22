import os
import re
import sys

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex for start and end of Gutenberg texts
    # This is a heuristic and might need adjustment for specific files
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG ETEXT .* \*\*\*",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG ETEXT .* \*\*\*",
    ]

    start_pos = 0
    end_pos = len(text)

    for marker in start_markers:
        match = re.search(marker, text)
        if match:
            start_pos = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, text)
        if match:
            end_pos = match.start()
            break

    cleaned_text = text[start_pos:end_pos].strip()

    # Check if cleaning actually happened (sanity check)
    if len(cleaned_text) == len(text):
        print(f"Warning: No Gutenberg markers found in {filepath}")
    else:
        print(f"Cleaned {filepath}: Removed {len(text) - len(cleaned_text)} characters")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_gutenberg.py <file1> <file2> ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        clean_gutenberg_text(filepath)
