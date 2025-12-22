import os
import re
import argparse

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from text.
    """
    # Common start and end markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    # Find start
    for i, line in enumerate(lines[:1000]): # Check first 1000 lines
        for marker in start_markers:
            if re.search(marker, line, re.IGNORECASE):
                start_idx = i + 1
                break
        if start_idx != 0:
            break

    # Find end
    for i, line in enumerate(lines[-1000:], start=max(0, len(lines)-1000)): # Check last 1000 lines
        for marker in end_markers:
            if re.search(marker, line, re.IGNORECASE):
                end_idx = i
                break
        if end_idx != len(lines):
            break

    # If markers not found, try to find license block at start
    if start_idx == 0:
        # Fallback: look for "Produced by" which often appears before the text
        for i, line in enumerate(lines[:500]):
             if line.startswith("Produced by"):
                 # often followed by some blank lines
                 start_idx = i + 1

    cleaned_lines = lines[start_idx:end_idx]
    return '\n'.join(cleaned_lines).strip()

def process_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaned_text = clean_gutenberg_text(text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Cleaned {filepath}. Length: {len(text)} -> {len(cleaned_text)}")

def main():
    parser = argparse.ArgumentParser(description="Clean Project Gutenberg headers/footers.")
    parser.add_argument("directory", help="Directory containing .txt files to clean.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory.")
        return

    for filename in os.listdir(args.directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(args.directory, filename)
            process_file(filepath)

if __name__ == "__main__":
    main()
