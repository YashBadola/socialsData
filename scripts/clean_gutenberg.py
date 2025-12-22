import os
import re
import argparse
import glob

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    """
    # Patterns for start and end of Gutenberg texts
    start_patterns = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK"
    ]

    end_patterns = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THIS PROJECT GUTENBERG EBOOK",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK"
    ]

    lines = text.splitlines()
    start_index = 0
    end_index = len(lines)

    # Find start
    for i, line in enumerate(lines):
        for pattern in start_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                start_index = i + 1
                break
        if start_index > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        if i < start_index:
            continue
        for pattern in end_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                end_index = i
                break
        if end_index < len(lines):
            break

    # Extract content
    content = lines[start_index:end_index]

    # Remove empty leading/trailing lines
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()

    return "\n".join(content)

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg headers/footers from text files.")
    parser.add_argument("files", nargs="+", help="File paths to clean")
    args = parser.parse_args()

    for file_pattern in args.files:
        for filepath in glob.glob(file_pattern):
            print(f"Cleaning {filepath}...")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()

                cleaned_text = clean_gutenberg_text(text)

                # Check if cleaning actually happened (basic check)
                if len(cleaned_text) == len(text):
                    print(f"Warning: No headers/footers found or removed in {filepath}")

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
