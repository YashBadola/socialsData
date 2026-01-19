import os
import requests
from pathlib import Path

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_dir = Path("socials_data/personalities/jean_jacques_rousseau/raw")
base_dir.mkdir(parents=True, exist_ok=True)

sources = [
    ("https://www.gutenberg.org/cache/epub/46333/pg46333.txt", "the_social_contract.txt"),
    ("https://www.gutenberg.org/cache/epub/3913/pg3913.txt", "confessions.txt"),
    ("https://www.gutenberg.org/cache/epub/5427/pg5427.txt", "emile.txt")
]

for url, filename in sources:
    download_file(url, base_dir / filename)
