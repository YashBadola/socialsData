import requests
import os
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}")
    response = requests.get(url)
    response.raise_for_status()
    # Handle BOM by decoding and encoding back to utf-8
    content = response.content.decode('utf-8-sig')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = "socials_data/personalities/william_james/raw"
os.makedirs(base_dir, exist_ok=True)

books = [
    {"id": "57628", "filename": "principles_psychology_vol1.txt"},
    {"id": "57634", "filename": "principles_psychology_vol2.txt"},
    {"id": "621", "filename": "varieties_religious_experience.txt"},
    {"id": "5116", "filename": "pragmatism.txt"},
    {"id": "5117", "filename": "meaning_of_truth.txt"}
]

for book in books:
    url = f"https://www.gutenberg.org/cache/epub/{book['id']}/pg{book['id']}.txt"
    filepath = os.path.join(base_dir, book['filename'])
    download_file(url, filepath)
    time.sleep(1) # Be nice to Gutenberg
