import requests
import os

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding
    content = response.content.decode('utf-8-sig') # Gutenberg often uses UTF-8 BOM

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done.")

def main():
    base_dir = "socials_data/personalities/plato/raw"
    os.makedirs(base_dir, exist_ok=True)

    files = {
        "the_republic.txt": "https://www.gutenberg.org/cache/epub/1497/pg1497.txt",
        "symposium.txt": "https://www.gutenberg.org/cache/epub/1600/pg1600.txt",
        "apology.txt": "https://www.gutenberg.org/cache/epub/1656/pg1656.txt"
    }

    for filename, url in files.items():
        filepath = os.path.join(base_dir, filename)
        try:
            download_file(url, filepath)
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    main()
