import os
import requests

DATA_DIR = "socials_data/personalities/aristotle/raw"

BOOKS = {
    "nicomachean_ethics": "8438",
    "politics": "6762",
    "poetics": "1974",
    "categories": "2412"
}

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig' # Important for Gutenberg
    if response.status_code == 200:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Success.")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    for name, pg_id in BOOKS.items():
        url = f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt"
        filepath = os.path.join(DATA_DIR, f"{name}.txt")
        download_file(url, filepath)

if __name__ == "__main__":
    main()
