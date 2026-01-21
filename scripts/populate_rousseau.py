import os
import requests

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"

# Ensure directory exists
os.makedirs(base_dir, exist_ok=True)

files = [
    ("https://www.gutenberg.org/ebooks/46333.txt.utf-8", "the_social_contract.txt"),
    ("https://www.gutenberg.org/ebooks/3913.txt.utf-8", "confessions.txt")
]

for url, filename in files:
    filepath = os.path.join(base_dir, filename)
    download_file(url, filepath)
