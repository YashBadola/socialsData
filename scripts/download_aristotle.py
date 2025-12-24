import os
import requests
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Done.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "socials_data", "personalities", "aristotle", "raw")
    os.makedirs(target_dir, exist_ok=True)

    books = {
        "nicomachean_ethics.txt": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
        "politics.txt": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
        "poetics.txt": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt",
        "categories.txt": "https://www.gutenberg.org/cache/epub/2412/pg2412.txt"
    }

    for filename, url in books.items():
        filepath = os.path.join(target_dir, filename)
        download_file(url, filepath)
        time.sleep(1) # Be nice to Gutenberg

if __name__ == "__main__":
    main()
