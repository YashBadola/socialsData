import requests
import os
from pathlib import Path

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle potential BOM
    content = response.content.decode('utf-8-sig')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done.")

def main():
    base_dir = Path("socials_data/personalities/immanuel_kant/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    sources = [
        ("https://www.gutenberg.org/cache/epub/4280/pg4280.txt", "critique_of_pure_reason.txt"),
        ("https://www.gutenberg.org/cache/epub/5683/pg5683.txt", "critique_of_practical_reason.txt"),
        ("https://www.gutenberg.org/cache/epub/48433/pg48433.txt", "critique_of_judgement.txt"),
        ("https://www.gutenberg.org/cache/epub/5682/pg5682.txt", "metaphysic_of_morals.txt")
    ]

    for url, filename in sources:
        download_file(url, base_dir / filename)

if __name__ == "__main__":
    main()
