import requests
import re
from pathlib import Path

def download_and_clean_text(url, output_path):
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    text = response.text

    # Basic cleaning for Project Gutenberg texts
    # Remove header
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"

    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index != -1:
        text = text[start_index + len(start_marker):]

    if end_index != -1:
        # Note: start_index is relative to original text, but after slicing,
        # indices shift. Ideally we find end_marker in the original or slice carefully.
        # But slicing from start makes end_index invalid if we don't recalculate.
        # Let's recalculate.
        end_index = text.find(end_marker)
        if end_index != -1:
            text = text[:end_index]

    # Trim whitespace
    text = text.strip()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved cleaned text to {output_path}")

if __name__ == "__main__":
    url = "https://www.gutenberg.org/cache/epub/8438/pg8438.txt"
    output_path = "socials_data/personalities/aristotle/raw/nicomachean_ethics.txt"
    download_and_clean_text(url, output_path)
