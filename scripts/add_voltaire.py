import os
import requests
import re
from pathlib import Path

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig' # Handle potential BOM
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_text(text, start_markers, end_markers):
    start_idx = 0
    end_idx = len(text)

    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            start_idx = idx + len(marker)
            print(f"Found start marker: {marker}")
            break
    else:
        print("Warning: No start marker found. Checking for generic headers...")
        # Fallback to looking for "START OF THE PROJECT" or similar
        match = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', text)
        if match:
             start_idx = match.end()
             print(f"Found generic start marker: {match.group(0)}")

    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_idx = idx
            print(f"Found end marker: {marker}")
            break
    else:
        print("Warning: No end marker found. Checking for generic footers...")
        match = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', text)
        if match:
             end_idx = match.start()
             print(f"Found generic end marker: {match.group(0)}")

    return text[start_idx:end_idx].strip()

def main():
    base_dir = Path("socials_data/personalities/voltaire/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    sources = [
        {
            "filename": "candide.txt",
            "url": "https://www.gutenberg.org/cache/epub/19942/pg19942.txt",
            "start_markers": ["*** START OF THIS PROJECT GUTENBERG EBOOK CANDIDE ***", "*** START OF THE PROJECT GUTENBERG EBOOK CANDIDE ***"],
            "end_markers": ["*** END OF THIS PROJECT GUTENBERG EBOOK CANDIDE ***", "*** END OF THE PROJECT GUTENBERG EBOOK CANDIDE ***"]
        },
        {
            "filename": "zadig.txt",
            "url": "https://www.gutenberg.org/cache/epub/18972/pg18972.txt",
            "start_markers": ["*** START OF THIS PROJECT GUTENBERG EBOOK ZADIG; OR, THE BOOK OF FATE ***"],
            "end_markers": ["*** END OF THIS PROJECT GUTENBERG EBOOK ZADIG; OR, THE BOOK OF FATE ***"]
        },
        {
            "filename": "philosophical_dictionary.txt",
            "url": "https://www.gutenberg.org/cache/epub/18569/pg18569.txt",
            "start_markers": ["*** START OF THIS PROJECT GUTENBERG EBOOK VOLTAIRE'S PHILOSOPHICAL DICTIONARY ***"],
            "end_markers": ["*** END OF THIS PROJECT GUTENBERG EBOOK VOLTAIRE'S PHILOSOPHICAL DICTIONARY ***"]
        }
    ]

    for source in sources:
        filepath = base_dir / source["filename"]
        download_file(source["url"], filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned_content = clean_text(content, source["start_markers"], source["end_markers"])

        # Additional cleaning for specific texts if needed (e.g. intro removal)
        # For now, we trust the markers.

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Processed {source['filename']}")

if __name__ == "__main__":
    main()
