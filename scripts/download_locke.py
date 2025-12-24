import requests
import os

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig' # Handle BOM if present
    if response.status_code == 200:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Success.")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

base_path = "socials_data/personalities/john_locke/raw"
os.makedirs(base_path, exist_ok=True)

files = [
    ("https://www.gutenberg.org/cache/epub/7370/pg7370.txt", "second_treatise_of_government.txt"),
    ("https://www.gutenberg.org/cache/epub/10615/pg10615.txt", "essay_human_understanding_vol1.txt"),
    ("https://www.gutenberg.org/cache/epub/10616/pg10616.txt", "essay_human_understanding_vol2.txt")
]

for url, filename in files:
    download_file(url, os.path.join(base_path, filename))
