import os
import requests

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Done.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        ("https://www.gutenberg.org/cache/epub/46333/pg46333.txt", "social_contract.txt"),
        ("https://www.gutenberg.org/cache/epub/3913/pg3913.txt", "confessions.txt"),
        ("https://www.gutenberg.org/cache/epub/5427/pg5427.txt", "emile.txt")
    ]

    for url, filename in sources:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            download_file(url, filepath)
        else:
            print(f"File already exists: {filepath}")

if __name__ == "__main__":
    main()
