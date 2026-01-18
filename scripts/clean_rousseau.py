import os
import requests
import sys

# Add the current directory to sys.path so we can import from scripts
sys.path.append(os.getcwd())

from scripts.clean_gutenberg import clean_gutenberg

DATA_DIR = "socials_data/personalities/jean_jacques_rousseau/raw"

files_to_download = [
    {
        "url": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
        "filename": "social_contract_and_discourses.txt"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
        "filename": "confessions.txt"
    }
]

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Try to detect encoding
    response.encoding = response.apparent_encoding

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Download complete.")

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for item in files_to_download:
        filepath = os.path.join(DATA_DIR, item["filename"])
        try:
            download_file(item["url"], filepath)
            clean_gutenberg(filepath)
        except Exception as e:
            print(f"Failed to process {item['filename']}: {e}")

if __name__ == "__main__":
    main()
