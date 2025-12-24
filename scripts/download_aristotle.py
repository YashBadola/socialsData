import os
import requests
from pathlib import Path

# URLs for Aristotle's works
FILES = {
    "nicomachean_ethics.txt": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
    "politics.txt": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
    "poetics.txt": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt",
    "the_categories.txt": "https://www.gutenberg.org/cache/epub/2412/pg2412.txt"
}

BASE_DIR = Path("socials_data/personalities/aristotle/raw")
BASE_DIR.mkdir(parents=True, exist_ok=True)

def download_file(filename, url):
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    # Handle BOM and encoding
    text = response.content.decode("utf-8-sig")

    file_path = BASE_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved to {file_path}")

def main():
    for filename, url in FILES.items():
        download_file(filename, url)

if __name__ == "__main__":
    main()
