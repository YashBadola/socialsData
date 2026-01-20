import os
import requests
from clean_gutenberg import clean_gutenberg

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        {
            "title": "The Social Contract",
            "url": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
            "filename": "the_social_contract.txt"
        },
        {
            "title": "Emile",
            "url": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt",
            "filename": "emile.txt"
        },
        {
            "title": "Confessions",
            "url": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
            "filename": "confessions.txt"
        }
    ]

    for source in sources:
        filepath = os.path.join(base_dir, source["filename"])
        if not os.path.exists(filepath):
            download_file(source["url"], filepath)
        else:
            print(f"File {filepath} already exists. Skipping download.")

        # Clean the file
        if os.path.exists(filepath):
            clean_gutenberg(filepath)

if __name__ == "__main__":
    main()
