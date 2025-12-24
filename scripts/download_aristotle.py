import os
import requests

def download_file(url, output_path):
    print(f"Downloading {url} to {output_path}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print("Download complete.")

def main():
    base_dir = os.path.join("socials_data", "personalities", "aristotle", "raw")
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        ("https://www.gutenberg.org/cache/epub/8438/pg8438.txt", "nicomachean_ethics.txt"),
        ("https://www.gutenberg.org/cache/epub/6762/pg6762.txt", "politics.txt"),
        ("https://www.gutenberg.org/cache/epub/1974/pg1974.txt", "poetics.txt")
    ]

    for url, filename in sources:
        output_path = os.path.join(base_dir, filename)
        if os.path.exists(output_path):
            print(f"File {filename} already exists. Skipping.")
        else:
            download_file(url, output_path)

if __name__ == "__main__":
    main()
