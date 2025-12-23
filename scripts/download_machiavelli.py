import requests
import os
import time

PERSONALITY_ID = "niccolo_machiavelli"
RAW_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"

BOOKS = {
    "the_prince.txt": "https://www.gutenberg.org/cache/epub/1232/pg1232.txt",
    "discourses_on_livy.txt": "https://www.gutenberg.org/cache/epub/10827/pg10827.txt",
    "art_of_war.txt": "https://www.gutenberg.org/cache/epub/15772/pg15772.txt"
}

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # Decode using utf-8-sig to handle BOM
        content = response.content.decode('utf-8-sig')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Directory {RAW_DIR} does not exist. Creating...")
        os.makedirs(RAW_DIR)

    for filename, url in BOOKS.items():
        filepath = os.path.join(RAW_DIR, filename)
        download_file(url, filepath)
        time.sleep(1) # Be nice to Gutenberg

if __name__ == "__main__":
    main()
