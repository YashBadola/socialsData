import os
import requests
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Use utf-8-sig to handle BOM if present
        content = response.content.decode('utf-8-sig')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "socials_data", "personalities", "aristotle", "raw")
    os.makedirs(target_dir, exist_ok=True)

    sources = [
        ("https://www.gutenberg.org/cache/epub/8438/pg8438.txt", "nicomachean_ethics.txt"),
        ("https://www.gutenberg.org/cache/epub/6762/pg6762.txt", "politics.txt"),
        ("https://www.gutenberg.org/cache/epub/1974/pg1974.txt", "poetics.txt")
    ]

    for url, filename in sources:
        filepath = os.path.join(target_dir, filename)
        if not os.path.exists(filepath):
            download_file(url, filepath)
            time.sleep(1) # Be nice to Gutenberg servers
        else:
            print(f"File {filename} already exists. Skipping.")

if __name__ == "__main__":
    main()
