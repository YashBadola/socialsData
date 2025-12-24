import os
import requests
from socials_data.core.manager import PersonalityManager

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding
    response.encoding = 'utf-8-sig'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Done.")

def main():
    manager = PersonalityManager()
    # We need to manually construct the raw directory path since the manager doesn't expose it directly for arbitrary purposes easily,
    # or we can assume the structure based on previous knowledge.
    # Ideally, we use the manager to find the base path.

    # Based on memory, manager.base_dir points to socials_data/personalities
    base_dir = manager.base_dir
    personality_dir = base_dir / "jean_jacques_rousseau"
    raw_dir = personality_dir / "raw"

    os.makedirs(raw_dir, exist_ok=True)

    files = {
        "the_social_contract.txt": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
        "emile.txt": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt",
        "the_confessions.txt": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt"
    }

    for filename, url in files.items():
        download_file(url, raw_dir / filename)

if __name__ == "__main__":
    main()
