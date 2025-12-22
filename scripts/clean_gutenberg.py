#!/usr/bin/env python3
import os
import sys
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for Start
    # Examples: "*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***", "*** START OF THIS PROJECT GUTENBERG EBOOK ..."
    start_pattern = r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*'

    # Pattern for End
    end_pattern = r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*'

    start_match = re.search(start_pattern, content)
    end_match = re.search(end_pattern, content)

    if start_match and end_match:
        start_index = start_match.end()
        end_index = end_match.start()
        cleaned_content = content[start_index:end_index].strip()

        # Additional cleaning: remove repeated newlines or strange artifacts if necessary
        # For now, just stripping the header/footer is the main goal.

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath}")
    else:
        print(f"Skipping {filepath}: Markers not found.")
        if not start_match:
            print("  - Start marker not found")
        if not end_match:
            print("  - End marker not found")

def main():
    if len(sys.argv) != 2:
        print("Usage: python clean_gutenberg.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            clean_file(os.path.join(directory, filename))

if __name__ == "__main__":
    main()
