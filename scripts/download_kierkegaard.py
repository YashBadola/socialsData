import os
import requests
import time

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    # URL for "Selections from the Writings of Kierkegaard"
    url = "https://www.gutenberg.org/cache/epub/60333/pg60333.txt"
    output_dir = "socials_data/personalities/soren_kierkegaard/raw"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "selections.txt")
    download_file(url, filepath)
