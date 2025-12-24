import requests
import os
import time

def download_file(url, filepath):
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Handle potential BOM and encoding issues
        content = response.content.decode('utf-8-sig')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_path = "socials_data/personalities/jean_jacques_rousseau/raw"
os.makedirs(base_path, exist_ok=True)

files = [
    ("https://www.gutenberg.org/cache/epub/46333/pg46333.txt", "the_social_contract.txt"),
    ("https://www.gutenberg.org/cache/epub/5427/pg5427.txt", "emile.txt"),
    ("https://www.gutenberg.org/cache/epub/3913/pg3913.txt", "the_confessions.txt"),
    ("https://www.gutenberg.org/cache/epub/11136/pg11136.txt", "discourse_on_inequality.txt")
]

for url, filename in files:
    download_file(url, os.path.join(base_path, filename))
    time.sleep(1) # Be nice to Gutenberg
