import os
import re
import argparse
from pathlib import Path

def strip_headers(text):
    """
    Tries to remove the Project Gutenberg headers and footers.
    Based on standard markers.
    """
    lines = text.splitlines()

    # Common markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\*START OF (THE|THIS) PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
        r"\*\*\*END OF (THE|THIS) PROJECT GUTENBERG EBOOK",
    ]

    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines):
        for marker in start_markers:
            if re.search(marker, line, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        for marker in end_markers:
            if re.search(marker, line, re.IGNORECASE):
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # If standard markers not found, look for "End of Project Gutenberg" variants
    if end_idx == len(lines):
         for i in range(len(lines) - 1, max(0, len(lines) - 500), -1):
             if "End of the Project Gutenberg" in lines[i] or "End of Project Gutenberg" in lines[i]:
                 end_idx = i
                 break

    return "\n".join(lines[start_idx:end_idx]).strip()

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback to latin-1 if utf-8 fails (though most PG are utf-8)
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()

    cleaned_content = strip_headers(content)

    # Overwrite the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"cleaned {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg texts.")
    parser.add_argument("directory", help="Directory containing .txt files to clean.")
    args = parser.parse_args()

    dir_path = Path(args.directory)
    if not dir_path.exists():
        print(f"Directory {dir_path} does not exist.")
        return

    for txt_file in dir_path.glob("*.txt"):
        clean_file(txt_file)

if __name__ == "__main__":
    main()
