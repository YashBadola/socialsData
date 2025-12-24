import os
import requests
import re
from pathlib import Path

# Constants
PERSONALITY_ID = "georg_wilhelm_friedrich_hegel"
BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID
RAW_DIR = BASE_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Sources
# (url, filename, start_marker, end_marker)
SOURCES = [
    (
        "https://www.gutenberg.org/cache/epub/39064/pg39064.txt",
        "philosophy_of_mind.txt",
        "THE PHILOSOPHY OF MIND",
        "End of the Project Gutenberg EBook"
    ),
    (
        "https://www.gutenberg.org/cache/epub/55108/pg55108.txt",
        "logic_of_hegel.txt",
        "THE LOGIC OF HEGEL", # Guessing
        "End of the Project Gutenberg EBook"
    ),
    (
        "https://www.gutenberg.org/cache/epub/51635/pg51635.txt",
        "lectures_history_philosophy_v1.txt",
        "HISTORY OF PHILOSOPHY",
        "End of the Project Gutenberg EBook"
    ),
    (
        "https://www.gutenberg.org/cache/epub/55334/pg55334.txt",
        "philosophy_of_fine_art_v1.txt",
        "THE PHILOSOPHY OF FINE ART", # Guessing
        "End of the Project Gutenberg EBook"
    )
]

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding
    response.encoding = 'utf-8-sig'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_text(text, start_marker, end_marker):
    # Normalize markers to find them easily? No, keep exact.
    # Gutenberg texts often have variations.

    # Simple slicing
    start_idx = text.find(start_marker)
    if start_idx == -1:
        # Try case insensitive?
        start_idx = text.lower().find(start_marker.lower())

    if start_idx == -1:
        print(f"WARNING: Start marker '{start_marker}' not found. Dumping head...")
        print(text[:500])
        return None

    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = text.lower().find(end_marker.lower())

    if end_idx == -1:
        print(f"WARNING: End marker '{end_marker}' not found. Dumping tail...")
        print(text[-500:])
        return None

    # Adjust start to include/exclude marker?
    # Usually we want to start *at* the title or just after.
    # The memory said "prioritize the first line of the actual content".
    # For now, let's include the marker as it is likely the title.

    clean_content = text[start_idx:end_idx]
    return clean_content

def main():
    for url, filename, start_marker, end_marker in SOURCES:
        filepath = RAW_DIR / filename
        download_file(url, filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = clean_text(content, start_marker, end_marker)

        if cleaned:
            print(f"Cleaned {filename} successfully. Length: {len(cleaned)}")
            # Overwrite with cleaned text
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
        else:
            print(f"FAILED to clean {filename}")

if __name__ == "__main__":
    main()
