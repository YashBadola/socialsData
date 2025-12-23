import os
import requests
from pathlib import Path

# URLs for Project Gutenberg texts (Plain Text UTF-8)
# Nicomachean Ethics: pg8438.txt
# Politics: pg6762.txt
# Poetics: pg1974.txt

URLS = {
    "nicomachean_ethics.txt": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
    "politics.txt": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
    "poetics.txt": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt"
}

OUTPUT_DIR = Path("socials_data/personalities/aristotle/raw")

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding explicitly if needed, but requests usually guesses well.
    # Gutenberg often uses UTF-8.
    response.encoding = 'utf-8-sig'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Done.")

def main():
    if not OUTPUT_DIR.exists():
        print(f"Creating directory {OUTPUT_DIR}")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in URLS.items():
        filepath = OUTPUT_DIR / filename
        try:
            download_file(url, filepath)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    main()
