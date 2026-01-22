import os
import requests
import time

def download_file(url, output_path):
    print(f"Downloading {url} to {output_path}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print("Success.")
    else:
        print(f"Failed with status code: {response.status_code}")

def main():
    base_dir = "socials_data/personalities/bertrand_russell/raw"
    os.makedirs(base_dir, exist_ok=True)

    sources = [
        {
            "url": "https://www.gutenberg.org/cache/epub/5827/pg5827.txt",
            "filename": "problems_of_philosophy.txt"
        },
        {
            "url": "https://www.gutenberg.org/cache/epub/2529/pg2529.txt",
            "filename": "analysis_of_mind.txt"
        },
        {
            "url": "https://www.gutenberg.org/cache/epub/25447/pg25447.txt",
            "filename": "mysticism_and_logic.txt"
        }
    ]

    for source in sources:
        filepath = os.path.join(base_dir, source["filename"])
        if not os.path.exists(filepath):
            download_file(source["url"], filepath)
            time.sleep(1) # Be nice to Gutenberg servers
        else:
            print(f"{filepath} already exists.")

if __name__ == "__main__":
    main()
