import os
import requests
import re
from pathlib import Path

# Config
PERSONALITY_ID = "plato"
RAW_DIR = Path(f"socials_data/personalities/{PERSONALITY_ID}/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "republic.txt": "https://www.gutenberg.org/cache/epub/1497/pg1497.txt",
    "apology_crito_phaedo.txt": "https://www.gutenberg.org/cache/epub/1656/pg1656.txt",
    "symposium.txt": "https://www.gutenberg.org/cache/epub/1600/pg1600.txt"
}

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    Strategies may vary, but usually they are delimited by specific strings.
    """
    # Regex for start
    # START OF THE PROJECT GUTENBERG EBOOK ...
    start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    if start_match:
        text = text[start_match.end():]

    # Regex for end
    # END OF THE PROJECT GUTENBERG EBOOK ...
    end_match = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text, re.IGNORECASE)
    if end_match:
        text = text[:end_match.start()]

    return text.strip()

def main():
    for filename, url in SOURCES.items():
        filepath = RAW_DIR / filename

        # Download
        try:
            download_file(url, filepath)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            continue

        # Read, Clean, Save
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            cleaned = clean_gutenberg_text(content)

            # Simple check to see if we actually removed something or if the markers weren't found
            if len(cleaned) == len(content):
                print(f"Warning: No Gutenberg markers found in {filename}.")
            else:
                print(f"Cleaned {filename} (reduced size from {len(content)} to {len(cleaned)} chars).")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
