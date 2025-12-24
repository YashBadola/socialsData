import os
import requests
import time

RAW_DIR = "socials_data/personalities/john_locke/raw"
FILES = {
    "second_treatise_of_government.txt": "https://www.gutenberg.org/cache/epub/7370/pg7370.txt",
    "essay_concerning_human_understanding_1.txt": "https://www.gutenberg.org/cache/epub/10615/pg10615.txt",
    "essay_concerning_human_understanding_2.txt": "https://www.gutenberg.org/cache/epub/10616/pg10616.txt"
}

os.makedirs(RAW_DIR, exist_ok=True)

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Handle BOM and encoding
        response.encoding = 'utf-8-sig'
        content = response.text

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {filepath}: {e}")

if __name__ == "__main__":
    for filename, url in FILES.items():
        filepath = os.path.join(RAW_DIR, filename)
        if not os.path.exists(filepath):
            download_file(url, filepath)
            time.sleep(1) # Be nice to Gutenberg
        else:
            print(f"{filepath} already exists.")
