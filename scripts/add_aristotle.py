import requests
import os
import re

def download_and_clean(url, filename, start_marker, end_marker):
    print(f"Downloading {filename}...")
    response = requests.get(url)
    response.encoding = 'utf-8-sig' # Handle BOM if present
    text = response.text

    print(f"Cleaning {filename}...")

    # Strip Gutenberg header/footer
    start_idx = text.find(start_marker)
    if start_idx == -1:
        # Fallback for some variations
        print(f"Warning: Start marker '{start_marker}' not found in {filename}. Dumping first 500 chars to debug.")
        print(text[:500])
        return

    end_idx = text.find(end_marker)
    if end_idx == -1:
        print(f"Warning: End marker '{end_marker}' not found in {filename}. Dumping last 500 chars to debug.")
        print(text[-500:])
        return

    # Adjust start index to skip the marker itself
    start_idx += len(start_marker)

    cleaned_text = text[start_idx:end_idx].strip()

    output_path = f"socials_data/personalities/aristotle/raw/{filename}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"Saved to {output_path}")

def main():
    # Nicomachean Ethics
    download_and_clean(
        "https://www.gutenberg.org/cache/epub/8438/pg8438.txt",
        "nicomachean_ethics.txt",
        "*** START OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE ETHICS OF ARISTOTLE ***"
    )

    # Politics
    download_and_clean(
        "https://www.gutenberg.org/cache/epub/6762/pg6762.txt",
        "politics.txt",
        "*** START OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK POLITICS: A TREATISE ON GOVERNMENT ***"
    )

    # Poetics
    download_and_clean(
        "https://www.gutenberg.org/cache/epub/1974/pg1974.txt",
        "poetics.txt",
        "*** START OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE POETICS OF ARISTOTLE ***"
    )

if __name__ == "__main__":
    main()
