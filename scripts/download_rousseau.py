import os
import requests

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
os.makedirs(base_dir, exist_ok=True)

files = [
    ("https://www.gutenberg.org/ebooks/46333.txt.utf-8", "the_social_contract_and_discourses.txt"),
    ("https://www.gutenberg.org/ebooks/3913.txt.utf-8", "the_confessions.txt")
]

for url, filename in files:
    filepath = os.path.join(base_dir, filename)
    download_file(url, filepath)
