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
        print(f"Successfully downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Base directory
base_dir = os.path.join("socials_data", "personalities", "ralph_waldo_emerson", "raw")
os.makedirs(base_dir, exist_ok=True)

# Sources
sources = [
    {
        "filename": "essays_first_series.txt",
        "url": "https://www.gutenberg.org/cache/epub/2944/pg2944.txt"
    },
    {
        "filename": "essays_second_series.txt",
        "url": "https://www.gutenberg.org/cache/epub/2945/pg2945.txt"
    },
    {
        "filename": "nature.txt",
        "url": "https://www.gutenberg.org/cache/epub/29433/pg29433.txt"
    },
    {
        "filename": "representative_men.txt",
        "url": "https://www.gutenberg.org/cache/epub/6312/pg6312.txt"
    },
    {
        "filename": "conduct_of_life.txt",
        "url": "https://www.gutenberg.org/cache/epub/39827/pg39827.txt"
    }
]

for source in sources:
    filepath = os.path.join(base_dir, source["filename"])
    # Always download to overwrite the wrong files
    download_file(source["url"], filepath)
    time.sleep(1) # Be nice to Gutenberg servers
