import requests
import re
from pathlib import Path

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    """
    # Common markers
    start_markers = [
        r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK, .* \*\*\*",
    ]
    end_markers = [
        r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    end_idx = len(text)

    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    for marker in end_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            end_idx = match.start()
            break

    content = text[start_idx:end_idx].strip()

    return content

def download_and_save(book_id, filename, dest_dir):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Gutenberg texts are often utf-8 with BOM
        response.encoding = 'utf-8-sig'
        text = response.text

        cleaned_text = clean_gutenberg_text(text)

        filepath = dest_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Saved {filename} to {filepath}")

    except Exception as e:
        print(f"Error processing {book_id}: {e}")

def main():
    base_dir = Path("socials_data/personalities/john_locke/raw")
    base_dir.mkdir(parents=True, exist_ok=True)

    books = [
        (7370, "second_treatise_of_government.txt"),
        (10615, "essay_concerning_human_understanding_vol1.txt"),
        (10616, "essay_concerning_human_understanding_vol2.txt")
    ]

    for book_id, filename in books:
        download_and_save(book_id, filename, base_dir)

if __name__ == "__main__":
    main()
