import os
import requests
import re
from pathlib import Path

# Setup paths
BASE_DIR = Path("socials_data/personalities/plato")
RAW_DIR = BASE_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Sources configuration
# We use specific start markers to strip Jowett's introductions.
SOURCES = [
    {
        "title": "The Republic",
        "url": "https://www.gutenberg.org/cache/epub/150/pg150.txt",
        "filename": "the_republic.txt",
        # "BOOK I" is a good start for the text proper
        "start_marker": "BOOK I",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "The Symposium",
        "url": "https://www.gutenberg.org/cache/epub/1600/pg1600.txt",
        "filename": "symposium.txt",
        # "PERSONS OF THE DIALOGUE" works for Symposium
        "start_marker": "PERSONS OF THE DIALOGUE",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "The Apology",
        "url": "https://www.gutenberg.org/cache/epub/1656/pg1656.txt",
        "filename": "apology.txt",
        # "How you, O Athenians" is the famous opening line.
        # But we can look for the second "APOLOGY" capitalized which serves as the title before the text
        # Or search for the specific first sentence fragment.
        "start_marker": "How you, O Athenians,",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    },
    {
        "title": "Phaedo",
        "url": "https://www.gutenberg.org/cache/epub/1658/pg1658.txt",
        "filename": "phaedo.txt",
        "start_marker": "PERSONS OF THE DIALOGUE",
        "end_marker": "END OF THE PROJECT GUTENBERG EBOOK"
    }
]

def clean_text(text, start_marker, end_marker):
    # First pass: Gutenberg headers
    # Usually starts with "*** START OF THE PROJECT" and ends with "*** END OF THE PROJECT"

    gutenberg_start_match = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', text)
    gutenberg_end_match = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*', text)

    start_idx = 0
    end_idx = len(text)

    if gutenberg_start_match:
        start_idx = gutenberg_start_match.end()

    if gutenberg_end_match:
        end_idx = gutenberg_end_match.start()

    content = text[start_idx:end_idx]

    # Second pass: Specific markers to skip introductions
    if start_marker:
        marker_idx = content.find(start_marker)
        if marker_idx != -1:
            # Check context: if it's too early, it might be TOC.
            # But for "PERSONS OF THE DIALOGUE" it's usually unique enough near the start of the play text.
            # For "BOOK I", it might appear in TOC.
            # In pg150.txt, "BOOK I" appears in TOC first.
            # We want the one that is followed by the text.
            # Let's find all occurrences and pick the one that looks like a header (surrounded by newlines)
            # or simply the last one if there are few?
            # Actually, "BOOK I" appears in "ARGUMENT" section too.
            # Let's try to find the one followed by "I went down yesterday to the Piraeus" (Republic opening).
            # Or just use the opening line for Republic?
            # "I went down yesterday to the Piraeus" is safer.

            if start_marker == "BOOK I":
                 # Special handling for Republic to avoid TOC
                 real_start = content.find("I went down yesterday to the Piraeus")
                 if real_start != -1:
                     # Go back a bit to include "BOOK I" if we want, or just start there.
                     # Starting at "I went down..." is cleaner.
                     content = content[real_start:]
                 else:
                     content = content[marker_idx:]
            else:
                 content = content[marker_idx:]

    return content.strip()

def download_and_process():
    print(f"Processing to {RAW_DIR}...")

    for source in SOURCES:
        print(f"Downloading {source['title']}...")
        try:
            response = requests.get(source['url'], timeout=30)
            response.raise_for_status()

            # Handle encoding - Gutenberg usually UTF-8
            text = response.content.decode('utf-8-sig')

            print(f"Cleaning {source['title']}...")
            cleaned_text = clean_text(text, source['start_marker'], source['end_marker'])

            out_path = RAW_DIR / source['filename']
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            print(f"Saved {source['filename']} ({len(cleaned_text)} chars)")

        except Exception as e:
            print(f"Failed to process {source['title']}: {e}")

if __name__ == "__main__":
    download_and_process()
