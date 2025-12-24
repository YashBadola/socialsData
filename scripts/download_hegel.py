import requests
import os
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Decode using utf-8-sig to handle BOM if present
        content = response.content.decode('utf-8-sig')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_dir = "socials_data/personalities/georg_wilhelm_friedrich_hegel/raw"
os.makedirs(base_dir, exist_ok=True)

files = {
    "philosophy_of_mind.txt": "https://www.gutenberg.org/cache/epub/39064/pg39064.txt",
    "history_of_philosophy_vol1.txt": "https://www.gutenberg.org/cache/epub/51635/pg51635.txt",
    "history_of_philosophy_vol2.txt": "https://www.gutenberg.org/cache/epub/51636/pg51636.txt",
    "history_of_philosophy_vol3.txt": "https://www.gutenberg.org/cache/epub/58169/pg58169.txt",
    "philosophy_of_fine_art_vol1.txt": "https://www.gutenberg.org/cache/epub/55334/pg55334.txt",
    "philosophy_of_fine_art_vol2.txt": "https://www.gutenberg.org/cache/epub/55445/pg55445.txt",
    "philosophy_of_fine_art_vol3.txt": "https://www.gutenberg.org/cache/epub/55623/pg55623.txt",
    "philosophy_of_fine_art_vol4.txt": "https://www.gutenberg.org/cache/epub/55731/pg55731.txt",
    "logic_of_hegel.txt": "https://www.gutenberg.org/cache/epub/55108/pg55108.txt",
    "intro_philosophy_of_fine_arts.txt": "https://www.gutenberg.org/cache/epub/46330/pg46330.txt"
}

for filename, url in files.items():
    filepath = os.path.join(base_dir, filename)
    download_file(url, filepath)
    time.sleep(1) # Be nice to Gutenberg servers
