import os
import requests

DATA_DIR = "socials_data/personalities/plato/raw"
os.makedirs(DATA_DIR, exist_ok=True)

sources = {
    "the_republic.txt": 1497,
    "symposium.txt": 1600,
    "apology.txt": 1656,
    "phaedo.txt": 1658
}

for filename, pg_id in sources.items():
    url = f"https://www.gutenberg.org/cache/epub/{pg_id}/pg{pg_id}.txt"
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # Handle encoding, usually utf-8-sig for Gutenberg
        text = response.content.decode('utf-8-sig')

        with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
