import os
import re
import argparse
import sys

def strip_headers(text):
    """
    Remove Project Gutenberg headers and footers from text.
    """
    lines = text.splitlines()

    # Common header markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG",
        r"\*\*\*START OF (THE|THIS) PROJECT GUTENBERG",
    ]

    # Common footer markers
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG",
        r"\*\*\*END OF (THE|THIS) PROJECT GUTENBERG",
    ]

    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines[:500]): # Search first 500 lines
        for marker in start_markers:
            if re.search(marker, line, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(reversed(lines)): # Search from end
        for marker in end_markers:
            if re.search(marker, line, re.IGNORECASE):
                end_idx = len(lines) - i - 1
                break
        if end_idx < len(lines):
            break

    return "\n".join(lines[start_idx:end_idx]).strip()

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaned_text = strip_headers(text)

    if len(cleaned_text) < 100:
        print(f"Warning: Cleaned text for {filepath} is very short ({len(cleaned_text)} chars). Check markers.")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Cleaned {filepath}. Length: {len(cleaned_text)} chars.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg texts.")
    parser.add_argument("files", nargs="+", help="Files to clean")
    args = parser.parse_args()

    for f in args.files:
        clean_file(f)
