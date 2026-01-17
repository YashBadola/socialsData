import os
import requests

DATA_DIR = "socials_data/personalities/bertrand_russell/raw"
os.makedirs(DATA_DIR, exist_ok=True)

books = {
    "problems_of_philosophy.txt": "https://www.gutenberg.org/cache/epub/5827/pg5827.txt",
    "analysis_of_mind.txt": "https://www.gutenberg.org/cache/epub/2529/pg2529.txt",
    "mysticism_and_logic.txt": "https://www.gutenberg.org/cache/epub/25447/pg25447.txt"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for filename, url in books.items():
    filepath = os.path.join(DATA_DIR, filename)
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Gutenberg text is often utf-8-sig or just utf-8.
        response.encoding = 'utf-8'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved {filepath}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
