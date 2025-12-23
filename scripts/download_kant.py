import os
import requests
from pathlib import Path

# Metadata
PERSONALITY_ID = "immanuel_kant"
SOURCES = [
    {"id": "4280", "filename": "critique_of_pure_reason.txt"},
    {"id": "5683", "filename": "critique_of_practical_reason.txt"},
    {"id": "48433", "filename": "critique_of_judgement.txt"}
]

# Paths
BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID / "raw"

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Done.")

def main():
    if not BASE_DIR.exists():
        print(f"Directory {BASE_DIR} does not exist.")
        return

    for source in SOURCES:
        url = f"https://www.gutenberg.org/cache/epub/{source['id']}/pg{source['id']}.txt"
        filepath = BASE_DIR / source["filename"]
        download_file(url, filepath)

if __name__ == "__main__":
    main()
