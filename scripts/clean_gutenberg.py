import os
import re
import argparse

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    """
    # Regex for start and end markers
    start_pattern = r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*'
    end_pattern = r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*'

    start_match = re.search(start_pattern, text, re.IGNORECASE)
    end_match = re.search(end_pattern, text, re.IGNORECASE)

    start_idx = 0
    end_idx = len(text)

    if start_match:
        start_idx = start_match.end()

    if end_match:
        end_idx = end_match.start()

    cleaned_text = text[start_idx:end_idx].strip()

    # Also remove the "Produced by..." lines that often follow the start marker
    cleaned_text = re.sub(r'Produced by .*(\r\n|\r|\n)', '', cleaned_text)

    return cleaned_text

def process_file(filepath, inplace=True):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    cleaned = clean_gutenberg_text(content)

    if len(cleaned) < len(content) * 0.1:
        print(f"Warning: Cleaning {filepath} resulted in very little text. Check the markers.")

    if inplace:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"Cleaned {filepath}")
    else:
        print(f"--- Cleaned content of {filepath} ---")
        print(cleaned[:500] + "...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg texts.")
    parser.add_argument("filepaths", nargs='+', help="Path to the text files")
    args = parser.parse_args()

    for fp in args.filepaths:
        process_file(fp)
