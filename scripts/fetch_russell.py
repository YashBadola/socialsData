import os
import urllib.request

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Downloaded {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
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
        },
        {
            "title": "Mysticism and Logic and Other Essays",
            "url": "https://www.gutenberg.org/cache/epub/25447/pg25447.txt",
            "filename": "mysticism_and_logic.txt"
        }
    ]

    for source in sources:
        filepath = os.path.join(base_dir, source["filename"])
        download_file(source["url"], filepath)

if __name__ == "__main__":
    main()
