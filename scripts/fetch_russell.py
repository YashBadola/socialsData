import requests
import os

def download_file(url, save_path):
    print(f"Downloading {url} to {save_path}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

base_dir = "socials_data/personalities/bertrand_russell/raw"
os.makedirs(base_dir, exist_ok=True)

sources = [
    {
        "title": "The Problems of Philosophy",
        "url": "https://www.gutenberg.org/cache/epub/5827/pg5827.txt",
        "filename": "problems_of_philosophy.txt"
    },
    {
        "title": "The Analysis of Mind",
        "url": "https://www.gutenberg.org/cache/epub/2529/pg2529.txt",
        "filename": "analysis_of_mind.txt"
    }
]

for source in sources:
    save_path = os.path.join(base_dir, source["filename"])
    download_file(source["url"], save_path)
