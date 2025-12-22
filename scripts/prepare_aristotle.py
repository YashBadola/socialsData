import os
import requests
import re
from pathlib import Path

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_gutenberg_text(text):
    # Common start/end markers
    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_pos = 0
    end_pos = len(text)

    for marker in start_markers:
        match = re.search(marker, text)
        if match:
            start_pos = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, text)
        if match:
            end_pos = match.start()
            break

    return text[start_pos:end_pos].strip()

def main():
    base_dir = Path("socials_data/personalities/aristotle/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    works = [
        {
            "id": "8438",
            "title": "nicomachean_ethics",
            "url": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt"
        },
        {
            "id": "6762",
            "title": "politics",
            "url": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt"
        },
        {
            "id": "1974",
            "title": "poetics",
            "url": "https://www.gutenberg.org/cache/epub/1974/pg1974.txt"
        }
    ]

    for work in works:
        filename = f"{work['title']}.txt"
        filepath = base_dir / filename

        # Download
        try:
            download_file(work['url'], filepath)

            # Read, Clean, Write back
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = clean_gutenberg_text(content)

            # Additional cleaning for specific texts if needed (e.g. intro removal)
            # For now, we stick to standard Gutenberg stripping.

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            print(f"Processed {filename}")

        except Exception as e:
            print(f"Failed to process {work['title']}: {e}")

if __name__ == "__main__":
    main()
