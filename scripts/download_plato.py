import requests
import os
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Done.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    base_dir = "socials_data/personalities/plato/raw"
    os.makedirs(base_dir, exist_ok=True)

    # Project Gutenberg URLs (using cache/epub format which is often more reliable/direct)
    # The Republic: https://www.gutenberg.org/ebooks/1497.txt.utf-8 or https://www.gutenberg.org/cache/epub/1497/pg1497.txt
    # The Symposium: https://www.gutenberg.org/ebooks/1600.txt.utf-8 or https://www.gutenberg.org/cache/epub/1600/pg1600.txt
    # The Apology: https://www.gutenberg.org/ebooks/1656.txt.utf-8 or https://www.gutenberg.org/cache/epub/1656/pg1656.txt

    books = [
        ("the_republic.txt", "https://www.gutenberg.org/cache/epub/1497/pg1497.txt"),
        ("the_symposium.txt", "https://www.gutenberg.org/cache/epub/1600/pg1600.txt"),
        ("the_apology.txt", "https://www.gutenberg.org/cache/epub/1656/pg1656.txt")
    ]

    for filename, url in books:
        filepath = os.path.join(base_dir, filename)
        download_file(url, filepath)
        time.sleep(1) # Be nice to the server

if __name__ == "__main__":
    main()
