import os
import requests
import time

def download_file(url, output_path):
    print(f"Downloading {url} to {output_path}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)
        print("Success.")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    base_dir = os.path.join("socials_data", "personalities", "bertrand_russell", "raw")
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
        output_path = os.path.join(base_dir, source["filename"])
        if not os.path.exists(output_path):
            success = download_file(source["url"], output_path)
            if success:
                # Be nice to the server
                time.sleep(1)
        else:
            print(f"{source['filename']} already exists.")

if __name__ == "__main__":
    main()
