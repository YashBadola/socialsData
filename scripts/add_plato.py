import os
import requests
import re
from pathlib import Path

# URLs for raw text files on Project Gutenberg
SOURCES = {
    "the_republic": "https://www.gutenberg.org/cache/epub/1497/pg1497.txt",
    "symposium": "https://www.gutenberg.org/cache/epub/1600/pg1600.txt",
    "apology": "https://www.gutenberg.org/cache/epub/1656/pg1656.txt",
    "phaedo": "https://www.gutenberg.org/cache/epub/1658/pg1658.txt",
}

BASE_DIR = Path("socials_data/personalities/plato/raw")

def download_file(url, filename):
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    # Use utf-8-sig to handle BOM if present
    response.encoding = 'utf-8-sig'
    return response.text

def clean_text(text, title):
    print(f"Cleaning {title}...")

    # Standard Gutenberg start/end markers
    # Different books might have slight variations, but these are common
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK",
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK",
    ]

    start_idx = -1
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            # Move past the marker line
            newline_idx = text.find("\n", idx)
            start_idx = newline_idx + 1
            break

    end_idx = -1
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_idx = idx
            break

    if start_idx == -1:
        print(f"Warning: Start marker not found for {title}. Check raw file.")
        # Fallback to beginning
        start_idx = 0

    if end_idx == -1:
        print(f"Warning: End marker not found for {title}. Check raw file.")
        # Fallback to end
        end_idx = len(text)

    content = text[start_idx:end_idx]

    # Additional cleanup: Remove translator's introduction if possible.
    # This usually requires manual inspection of where the actual text starts.
    # For now, we will trust the Gutenberg markers but we might need to refine.
    # Let's try to find the specific title in the content to skip intros.

    real_start_markers = {
        "the_republic": ["THE REPUBLIC", "INTRODUCTION AND ANALYSIS"], # Jowett usually has a long intro.
        "symposium": ["SYMPOSIUM", "INTRODUCTION."],
        "apology": ["APOLOGY", "INTRODUCTION."],
        "phaedo": ["PHAEDO", "INTRODUCTION."]
    }

    # For Jowett translations, there's often a huge "INTRODUCTION AND ANALYSIS".
    # We might want to keep it as it's valuable context, or remove it to get just the dialogue.
    # "The philosopher's dataset" might imply we want the philosophy, which includes the analysis?
    # Usually, we want the primary text.
    # However, automatically stripping the intro is hard without specific markers.
    # Let's stick to the Gutenberg bounds for now, and maybe refine if we see too much noise.

    return content.strip()

def main():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)

    for name, url in SOURCES.items():
        try:
            raw_text = download_file(url, name)
            cleaned_text = clean_text(raw_text, name)

            output_path = BASE_DIR / f"{name}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            print(f"Saved {output_path}")

        except Exception as e:
            print(f"Error processing {name}: {e}")

if __name__ == "__main__":
    main()
