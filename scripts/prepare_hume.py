import os
import requests
import re
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    This is a heuristic approach and might need adjustment for specific files.
    """
    lines = text.split('\n')
    start_idx = 0
    end_idx = len(lines)

    # Common start markers
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
    ]

    # Common end markers
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
    ]

    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker in line:
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Search from the end
    for i in range(len(lines) - 1, -1, -1):
        for marker in end_markers:
            if marker in lines[i]:
                end_idx = i
                break
        if end_idx < len(lines):
            break

    # If markers not found, try to look for license/header blocks heuristically
    # (Leaving simple for now, usually the markers are there)

    content = '\n'.join(lines[start_idx:end_idx])
    return content.strip()

def download_and_clean(url, filename, output_dir):
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    response.raise_for_status()

    raw_text = response.text
    cleaned_text = clean_gutenberg_text(raw_text)

    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    print(f"Saved to {output_path}")

def main():
    base_dir = Path("socials_data/personalities/david_hume/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    # A Treatise of Human Nature
    download_and_clean(
        "https://www.gutenberg.org/cache/epub/4705/pg4705.txt",
        "treatise_of_human_nature.txt",
        base_dir
    )

    # An Enquiry Concerning Human Understanding
    download_and_clean(
        "https://www.gutenberg.org/cache/epub/9662/pg9662.txt",
        "enquiry_human_understanding.txt",
        base_dir
    )

if __name__ == "__main__":
    main()
