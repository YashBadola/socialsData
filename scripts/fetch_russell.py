import requests
import os

def download_file(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    # Gutenberg text encoding is usually UTF-8
    response.encoding = 'utf-8'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} to {filepath}")

base_dir = "socials_data/personalities/bertrand_russell/raw"
os.makedirs(base_dir, exist_ok=True)

files = [
    ("https://www.gutenberg.org/cache/epub/5827/pg5827.txt", "problems_of_philosophy.txt"),
    ("https://www.gutenberg.org/cache/epub/2529/pg2529.txt", "analysis_of_mind.txt")
]

for url, filename in files:
    filepath = os.path.join(base_dir, filename)
    try:
        download_file(url, filepath)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
