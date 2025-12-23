import os
import re
from pathlib import Path

# Metadata
PERSONALITY_ID = "immanuel_kant"
FILES = [
    "critique_of_pure_reason.txt",
    "critique_of_practical_reason.txt",
    "critique_of_judgement.txt"
]

# Paths
BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID / "raw"

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Generic Gutenberg cleaning
    # Look for "START OF THE PROJECT GUTENBERG EBOOK" and "END OF THE PROJECT GUTENBERG EBOOK"
    # or variations.

    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    end_idx = len(content)

    for marker in start_markers:
        match = re.search(marker, content)
        if match:
            start_idx = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, content)
        if match:
            end_idx = match.start()
            break

    # Extract the core text
    text = content[start_idx:end_idx]

    # Further refinement: remove the license preamble if it stuck around
    # Often there's a few lines after the start marker before the actual text.
    # For now, just stripping whitespace is a safe bet.
    text = text.strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print("Done.")

def main():
    if not BASE_DIR.exists():
        print(f"Directory {BASE_DIR} does not exist.")
        return

    for filename in FILES:
        filepath = BASE_DIR / filename
        if filepath.exists():
            clean_file(filepath)
        else:
            print(f"File {filepath} not found.")

if __name__ == "__main__":
    main()
