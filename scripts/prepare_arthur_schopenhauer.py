import os
import requests
import re
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers from the text.
    This is a basic implementation and might need adjustment for specific texts.
    """
    # Start markers
    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"START OF THE PROJECT GUTENBERG EBOOK",
        r"START OF THIS PROJECT GUTENBERG EBOOK",
    ]

    # End markers
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"END OF THE PROJECT GUTENBERG EBOOK",
        r"END OF THIS PROJECT GUTENBERG EBOOK",
    ]

    start_pos = 0
    end_pos = len(text)

    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            start_pos = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            end_pos = match.start()
            break

    return text[start_pos:end_pos].strip()

def download_and_save(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()

    text = response.text
    cleaned_text = clean_gutenberg_text(text)

    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

def main():
    base_dir = Path("socials_data/personalities/arthur_schopenhauer/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    # The World as Will and Idea, Vol. 1
    # Gutenberg ID 38427
    url1 = "https://www.gutenberg.org/cache/epub/38427/pg38427.txt"
    download_and_save(url1, base_dir / "the_world_as_will_and_idea_vol1.txt")

    # Essays of Schopenhauer
    # Gutenberg ID 10732
    url2 = "https://www.gutenberg.org/cache/epub/10732/pg10732.txt"
    download_and_save(url2, base_dir / "essays_of_schopenhauer.txt")

    print("Download and preparation complete.")

if __name__ == "__main__":
    main()
