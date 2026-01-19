import os
import requests

def download_file(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} to {filepath}")

base_dir = os.path.join("socials_data", "personalities", "jean_jacques_rousseau", "raw")
os.makedirs(base_dir, exist_ok=True)

files = [
    {
        "url": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
        "filename": "social_contract.txt"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/11136/pg11136.txt",
        "filename": "discourse_on_inequality.txt"
    }
]

for item in files:
    filepath = os.path.join(base_dir, item["filename"])
    print(f"Downloading {item['filename']}...")
    try:
        download_file(item["url"], filepath)
    except Exception as e:
        print(f"Failed to download {item['filename']}: {e}")
