import os
import requests
import re
from pathlib import Path

# Metadata for download
PERSONALITY_ID = "rene_descartes"
SOURCES = [
    {"url": "https://www.gutenberg.org/cache/epub/59/pg59.txt", "filename": "discourse_on_method.txt"},
    {"url": "https://www.gutenberg.org/cache/epub/70091/pg70091.txt", "filename": "meditations.txt"},
    {"url": "https://www.gutenberg.org/cache/epub/4391/pg4391.txt", "filename": "principles_of_philosophy.txt"}
]

BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID / "raw"

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    This is a heuristic approach and might need adjustment per file.
    """
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    # Common start markers
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Find start
    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker in line:
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        for marker in end_markers:
            if marker in line:
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # If markers not found, try to look for license text at the end
    # but for now we stick to markers.

    clean_lines = lines[start_idx:end_idx]
    return "\n".join(clean_lines).strip()

def main():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True, exist_ok=True)

    for source in SOURCES:
        filepath = BASE_DIR / source["filename"]
        download_file(source["url"], filepath)

        # Clean the file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_gutenberg_text(content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Cleaned {filepath}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
