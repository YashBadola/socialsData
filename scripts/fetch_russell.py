import os
import urllib.request
import urllib.error

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        # User-Agent might be needed for some sites, but Gutenberg is usually fine.
        # Adding one just in case.
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
             content = response.read()
             with open(filepath, 'wb') as f:
                 f.write(content)
        print(f"Downloaded {filepath}")
    except urllib.error.URLError as e:
        print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    base_dir = "socials_data/personalities/bertrand_russell/raw"
    os.makedirs(base_dir, exist_ok=True)

    files = [
        ("https://www.gutenberg.org/cache/epub/5827/pg5827.txt", "problems_of_philosophy.txt"),
        ("https://www.gutenberg.org/cache/epub/2529/pg2529.txt", "analysis_of_mind.txt")
    ]

    for url, filename in files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            download_file(url, filepath)
        else:
            print(f"File {filepath} already exists.")

if __name__ == "__main__":
    main()
