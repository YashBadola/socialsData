import os
import requests

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
    os.makedirs(base_dir, exist_ok=True)

    files = [
        ("https://www.gutenberg.org/cache/epub/46333/pg46333.txt", "the_social_contract.txt"),
        ("https://www.gutenberg.org/cache/epub/3913/pg3913.txt", "confessions.txt")
    ]

    for url, filename in files:
        dest_path = os.path.join(base_dir, filename)
        if not os.path.exists(dest_path):
            download_file(url, dest_path)
        else:
            print(f"{filename} already exists.")

if __name__ == "__main__":
    main()
