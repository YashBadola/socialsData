import os
import requests
from pathlib import Path
from clean_gutenberg import clean_file

PERSONALITY_ID = "david_hume"
BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID
RAW_DIR = BASE_DIR / "raw"

# Gutenberg IDs
# 4705: A Treatise of Human Nature
# 9662: An Enquiry Concerning Human Understanding
# Using cache/epub URLs which are usually more stable for text
BOOKS = {
    "treatise_of_human_nature.txt": "https://www.gutenberg.org/cache/epub/4705/pg4705.txt",
    "enquiry_concerning_human_understanding.txt": "https://www.gutenberg.org/cache/epub/9662/pg9662.txt"
}

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Gutenberg texts are usually utf-8
        response.encoding = 'utf-8'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        raise

def prepare():
    if not RAW_DIR.exists():
        RAW_DIR.mkdir(parents=True)

    for filename, url in BOOKS.items():
        filepath = RAW_DIR / filename
        # Overwrite check: if it exists, we might want to ensure it's correct,
        # but for now let's just assume if it's there it's good,
        # EXCEPT we failed last time so 9662 might not be there.
        if not filepath.exists():
            download_file(url, filepath)
            clean_file(filepath)
        else:
            print(f"{filename} already exists. Skipping download.")

if __name__ == "__main__":
    prepare()
