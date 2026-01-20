import requests
import os

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

base_dir = "socials_data/personalities/bertrand_russell/raw"
os.makedirs(base_dir, exist_ok=True)

files = {
    "problems_of_philosophy.txt": "https://www.gutenberg.org/cache/epub/5827/pg5827.txt",
    "analysis_of_mind.txt": "https://www.gutenberg.org/cache/epub/2529/pg2529.txt"
}

for filename, url in files.items():
    filepath = os.path.join(base_dir, filename)
    download_file(url, filepath)
