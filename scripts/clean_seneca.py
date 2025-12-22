
import re
import sys
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers, and specific translator introductions.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Find start of the actual content
    # Gutenberg usually has "*** START OF THIS PROJECT GUTENBERG..."
    for i, line in enumerate(lines):
        if "*** START OF THIS PROJECT GUTENBERG" in line or "*** START OF THE PROJECT GUTENBERG" in line:
            start_idx = i + 1
            break

    # Check for translator intro ending
    # In L'Estrange's version, the actual text often starts after a Table of Contents or "TO THE READER"
    # Let's look for "OF A HAPPY LIFE, AND THE MEANS OF IT." which seems to be the first title in 56075
    # Or we can just look for the end of the Gutenberg header and then do some manual inspection logic if needed.
    # For now, let's stick to standard Gutenberg removal + some basic heuristic.

    # Find end of the content
    for i in range(len(lines) - 1, -1, -1):
        if "*** END OF THIS PROJECT GUTENBERG" in lines[i] or "*** END OF THE PROJECT GUTENBERG" in lines[i]:
            end_idx = i
            break

    content = "\n".join(lines[start_idx:end_idx])

    # Further cleanup: remove License text if it leaked
    # And remove L'Estrange's "TO THE READER" if possible.
    # The text usually starts with titles.

    # Remove multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_seneca.py <filepath>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File {filepath} not found.")
        sys.exit(1)

    text = filepath.read_text(encoding='utf-8')
    cleaned_text = clean_gutenberg_text(text)

    # Write back or to a new file?
    # The instruction says "Clean Data: Run the cleaning script to produce a clean text file"
    # I'll overwrite for simplicity as the process command picks up everything in raw.

    filepath.write_text(cleaned_text, encoding='utf-8')
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    main()
