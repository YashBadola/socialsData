import os
import requests
import re
from pathlib import Path

# Metadata for download
KANT_WORKS = [
    {
        "title": "The Critique of Pure Reason",
        "id": "4280",
        "url": "https://www.gutenberg.org/cache/epub/4280/pg4280.txt",
        "start_marker": "Preface to the First Edition", # Changed from Title to Preface to be safe
        "end_marker": "*** END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "The Critique of Practical Reason",
        "id": "5683",
        "url": "https://www.gutenberg.org/cache/epub/5683/pg5683.txt",
        "start_marker": "CRITIQUE OF PRACTICAL REASON",
        "end_marker": "*** END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "The Critique of Judgement",
        "id": "48433",
        "url": "https://www.gutenberg.org/cache/epub/48433/pg48433.txt",
        "start_marker": "We may call the faculty of cognition from principles",
        "end_marker": "*** END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "Fundamental Principles of the Metaphysic of Morals",
        "id": "5682",
        "url": "https://www.gutenberg.org/cache/epub/5682/pg5682.txt",
        "start_marker": "FUNDAMENTAL PRINCIPLES OF THE METAPHYSIC OF MORALS",
        "end_marker": "*** END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "Prolegomena to Any Future Metaphysics",
        "id": "52821",
        "url": "https://www.gutenberg.org/cache/epub/52821/pg52821.txt",
        "start_marker": "INTRODUCTION.",
        "end_marker": "*** END OF THE PROJECT GUTENBERG EBOOK"
    }
]

BASE_DIR = Path("socials_data/personalities/immanuel_kant/raw")

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    response = requests.get(url)
    response.raise_for_status()
    # Handle encoding explicitly if possible, but requests usually guesses well.
    # Gutenberg text files often start with a BOM.
    response.encoding = 'utf-8-sig'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response.text)

def clean_text(text, start_marker, end_marker):
    # Find specific marker index first
    start_idx = text.find(start_marker)

    # Try finding Gutenberg header
    gutenberg_start_match = re.search(r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)

    if gutenberg_start_match:
        # If header found, chop it off
        text = text[gutenberg_start_match.end():]
        # Now try to find the specific marker in the remaining text
        inner_start = text.find(start_marker)
        if inner_start != -1:
            text = text[inner_start:]
    elif start_idx != -1:
        # Fallback: regex failed, but we found the specific marker, so start from there
        text = text[start_idx:]
    else:
        print(f"Warning: neither Gutenberg header nor start marker '{start_marker}' found properly at start.")

    # Handle End Marker
    end_idx = text.find(end_marker)
    if end_idx == -1:
         # Try regex for end if exact string fails
         match_end = re.search(r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*", text)
         if match_end:
             end_idx = match_end.start()

    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()

def main():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)

    for work in KANT_WORKS:
        filename = work['title'].lower().replace(" ", "_") + ".txt"
        filepath = BASE_DIR / filename

        # Download (or just read if exists, but we want to ensure fresh clean)
        # To save bandwidth/time if already downloaded and we just want to reclean:
        if not filepath.exists():
            download_file(work['url'], filepath)
        else:
             # Just for this session, I force download to ensure I don't process a truncated file from previous run.
             # In production, check exists is better.
             # But here I know I messed it up.
             download_file(work['url'], filepath)

        # Read
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean
        cleaned_content = clean_text(content, work['start_marker'], work['end_marker'])

        # Write back (or overwrite)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        print(f"Processed {work['title']}")

if __name__ == "__main__":
    main()
