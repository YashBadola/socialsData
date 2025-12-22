import os
import re

def clean_gutenberg_text(text):
    """
    Removes standard Project Gutenberg headers and footers.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Find start marker
    for i, line in enumerate(lines[:1000]): # Check first 1000 lines
        if "START OF THE PROJECT GUTENBERG EBOOK" in line or "START OF THIS PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
            break

    # Find end marker
    for i, line in enumerate(reversed(lines)): # Check from end
        if "END OF THE PROJECT GUTENBERG EBOOK" in line or "END OF THIS PROJECT GUTENBERG EBOOK" in line:
            end_idx = len(lines) - i - 1
            break

    # If standard markers are not found, look for license block at the end
    if end_idx == len(lines):
         # Fallback for end marker: look for "End of the Project Gutenberg"
         for i, line in enumerate(reversed(lines)):
             if "End of the Project Gutenberg" in line:
                 end_idx = len(lines) - i - 1
                 break

    return "\n".join(lines[start_idx:end_idx]).strip()

def process_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    cleaned_content = clean_gutenberg_text(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print("Done.")

def main():
    # Allow passing a specific file or directory, default to current logic if needed
    # For now, let's just make it a library or run it on specific files if arguments are passed.
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                for file in files:
                    if file.endswith(".txt"):
                        process_file(os.path.join(root, file))
        elif os.path.isfile(target):
            process_file(target)
    else:
        print("Usage: python scripts/clean_gutenberg.py <file_or_directory>")

if __name__ == "__main__":
    main()
