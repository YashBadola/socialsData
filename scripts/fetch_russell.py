import requests
import os

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        f.write(response.content)
    print("Done.")

base_dir = "socials_data/personalities/bertrand_russell/raw"
os.makedirs(base_dir, exist_ok=True)

files = [
    ("https://www.gutenberg.org/cache/epub/5827/pg5827.txt", "problems_of_philosophy.txt"),
    ("https://www.gutenberg.org/cache/epub/2529/pg2529.txt", "analysis_of_mind.txt")
]

for url, filename in files:
    dest_path = os.path.join(base_dir, filename)
    download_file(url, dest_path)
