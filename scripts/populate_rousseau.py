import os
import requests

DATA_DIR = "socials_data/personalities/jean_jacques_rousseau/raw"

files_to_download = {
    "confessions.txt": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
    "social_contract.txt": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
    "emile.txt": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt"
}

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Success.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for filename, url in files_to_download.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            download_file(url, filepath)
        else:
            print(f"{filename} already exists.")
