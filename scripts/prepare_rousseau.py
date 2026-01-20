import os
import requests
import sys

# Ensure we can import from scripts if running from root
sys.path.append(os.getcwd())

try:
    from scripts.clean_gutenberg import clean_gutenberg
except ImportError:
    # Fallback if running from scripts directory
    sys.path.append(os.path.join(os.getcwd(), '..'))
    from scripts.clean_gutenberg import clean_gutenberg

# URLs
files = {
    "confessions.txt": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
    "discourse_inequality.txt": "https://www.gutenberg.org/cache/epub/11136/pg11136.txt",
    "emile.txt": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt"
}

output_dir = "socials_data/personalities/jean_jacques_rousseau/raw"

def download_file(url, filepath):
    if os.path.exists(filepath):
        print(f"File {filepath} already exists. Skipping download.")
        return

    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename, url in files.items():
        filepath = os.path.join(output_dir, filename)
        download_file(url, filepath)
        print(f"Cleaning {filepath}...")
        clean_gutenberg(filepath)

if __name__ == "__main__":
    main()
