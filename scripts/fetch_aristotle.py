import os
import requests
import re

def clean_gutenberg_text(text):
    # Find the start of the book (flexible patterns)
    start_pattern = r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*"
    match_start = re.search(start_pattern, text)
    if match_start:
        text = text[match_start.end():]

    # Find the end of the book
    end_pattern = r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*"
    match_end = re.search(end_pattern, text)
    if match_end:
        text = text[:match_end.start()]

    # Strip extra whitespace
    return text.strip()

def main():
    books = [
        {
            "url": "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
            "filename": "nicomachean_ethics.txt"
        },
        {
            "url": "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
            "filename": "politics.txt"
        }
    ]

    output_dir = "socials_data/personalities/aristotle/raw/"
    os.makedirs(output_dir, exist_ok=True)

    for book in books:
        print(f"Fetching {book['url']}...")
        try:
            response = requests.get(book["url"])
            response.raise_for_status()
            text = response.text

            cleaned_text = clean_gutenberg_text(text)

            filepath = os.path.join(output_dir, book["filename"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved cleaned text to {filepath}")

        except Exception as e:
            print(f"Error processing {book['url']}: {e}")

if __name__ == "__main__":
    main()
