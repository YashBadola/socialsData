import os
import requests
import shutil

PERSONALITY_ID = "william_james"
RAW_DIR = os.path.join("socials_data", "personalities", PERSONALITY_ID, "raw")

SOURCES = [
    {
        "id": "5116",
        "filename": "pragmatism.txt",
        "url": "https://www.gutenberg.org/cache/epub/5116/pg5116.txt"
    },
    {
        "id": "621",
        "filename": "varieties_of_religious_experience.txt",
        "url": "https://www.gutenberg.org/cache/epub/621/pg621.txt"
    },
    {
        "id": "26659",
        "filename": "will_to_believe.txt",
        "url": "https://www.gutenberg.org/cache/epub/26659/pg26659.txt"
    }
]

def download_file(url, filepath):
    if os.path.exists(filepath):
        print(f"{filepath} already exists, skipping download.")
        return
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Done.")

def main():
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)

    for source in SOURCES:
        filepath = os.path.join(RAW_DIR, source["filename"])
        download_file(source["url"], filepath)

if __name__ == "__main__":
    main()
