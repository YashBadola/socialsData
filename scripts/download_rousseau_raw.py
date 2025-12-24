import requests
import os

files = {
    "social_contract_and_discourses.txt": "https://www.gutenberg.org/cache/epub/46333/pg46333.txt",
    "confessions.txt": "https://www.gutenberg.org/cache/epub/3913/pg3913.txt",
    "emile.txt": "https://www.gutenberg.org/cache/epub/5427/pg5427.txt"
}

output_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
os.makedirs(output_dir, exist_ok=True)

for filename, url in files.items():
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding explicitly if needed, but requests usually guesses well.
    # Gutenberg text files are usually UTF-8.
    response.encoding = 'utf-8-sig'

    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Saved {filename}")
