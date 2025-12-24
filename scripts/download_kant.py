import os
import requests
import time

PERSONALITY_DIR = "socials_data/personalities/immanuel_kant/raw"
os.makedirs(PERSONALITY_DIR, exist_ok=True)

BOOKS = [
    {"id": 4280, "filename": "critique_of_pure_reason.txt"},
    {"id": 5683, "filename": "critique_of_practical_reason.txt"},
    {"id": 48433, "filename": "critique_of_judgement.txt"},
    {"id": 5682, "filename": "metaphysic_of_morals.txt"},
    {"id": 52821, "filename": "prolegomena.txt"},
]

def download_book(book_id, filename):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    filepath = os.path.join(PERSONALITY_DIR, filename)
    print(f"Downloading {filename} from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Handle encoding
        content = response.content.decode('utf-8-sig')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    for book in BOOKS:
        download_book(book["id"], book["filename"])
        time.sleep(1) # Be nice to Gutenberg
