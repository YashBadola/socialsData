import os
import requests
import time

PERSONALITY_ID = "plato"
RAW_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"

BOOKS = [
    {"title": "the_republic", "id": "1497"},
    {"title": "symposium", "id": "1600"},
    {"title": "apology", "id": "1656"},
    {"title": "phaedo", "id": "1658"},
]

def download_book(book):
    url = f"https://www.gutenberg.org/cache/epub/{book['id']}/pg{book['id']}.txt"
    filepath = os.path.join(RAW_DIR, f"{book['title']}.txt")

    print(f"Downloading {book['title']} from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    # Handle BOM if present
    response.encoding = 'utf-8-sig'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Saved to {filepath}")
    time.sleep(1) # Be nice to Gutenberg

if __name__ == "__main__":
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)

    for book in BOOKS:
        download_book(book)
