import os
from pathlib import Path

RAW_DIR = Path("socials_data/personalities/aristotle/raw")

def clean_text(text):
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Heuristic to find start and end of Gutenberg texts
    for i, line in enumerate(lines):
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line or "*** START OF THIS PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in line or "*** END OF THIS PROJECT GUTENBERG EBOOK" in line:
            end_idx = i
            break

    # Refine start: often there is a preamble before the actual text starts after the Gutenberg header
    # But usually just stripping the header is enough for a first pass.
    # Let's try to be a bit smarter if we can, or just accept the license stuff is gone.

    content = "\n".join(lines[start_idx:end_idx]).strip()
    return content

def main():
    for filepath in RAW_DIR.glob("*.txt"):
        print(f"Cleaning {filepath.name}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()

        cleaned_content = clean_text(raw_content)

        # Save back to the same file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filepath.name} (length: {len(cleaned_content)} chars).")

if __name__ == "__main__":
    main()
