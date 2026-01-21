import requests
import os

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
os.makedirs(base_dir, exist_ok=True)

sources = [
    ("https://www.gutenberg.org/ebooks/46333.txt.utf-8", "the_social_contract.txt"),
    ("https://www.gutenberg.org/ebooks/3913.txt.utf-8", "confessions.txt"),
    ("https://www.gutenberg.org/ebooks/5427.txt.utf-8", "emile.txt")
]

for url, filename in sources:
    filepath = os.path.join(base_dir, filename)
    download_file(url, filepath)
