import os
import re
import argparse

def clean_gutenberg_text(text):
    """
    Strips Project Gutenberg headers and footers from text.
    """
    # Common markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
    ]

    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines[:1000]): # Search first 1000 lines
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

    # If no markers found, return original (or handle differently)
    # But usually Gutenberg texts have them.

    # Trim empty lines around the content
    content = lines[start_idx:end_idx]

    # Remove extra whitespace at start/end of content
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()

    return "\n".join(content)

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg texts.")
    parser.add_argument("directory", help="Directory containing .txt files to clean.")
    args = parser.parse_args()

    directory = args.directory
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            print(f"Cleaning {filename}...")

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            cleaned_text = clean_gutenberg_text(text)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"Cleaned {filename} (len: {len(text)} -> {len(cleaned_text)})")

if __name__ == "__main__":
    main()
