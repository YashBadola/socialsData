import os
import requests
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "socials_data", "personalities", "aristotle", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# Aristotle's Works
# Nicomachean Ethics: 8438
# Politics: 6762
# Poetics: 1974

files = {
    "nicomachean_ethics.txt": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
    "politics.txt": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
    "poetics.txt": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt"
}

for filename, url in files.items():
    filepath = os.path.join(RAW_DIR, filename)
    download_file(url, filepath)
    time.sleep(1) # Be nice to Gutenberg servers
