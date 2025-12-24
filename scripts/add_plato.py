import os
import requests
import re

# Directory
RAW_DIR = "socials_data/personalities/plato/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# URLs
SOURCES = {
    "the_republic.txt": "https://www.gutenberg.org/cache/epub/1497/pg1497.txt",
    "symposium.txt": "https://www.gutenberg.org/cache/epub/1600/pg1600.txt",
    "apology.txt": "https://www.gutenberg.org/cache/epub/1656/pg1656.txt"
}

def clean_text(text, filename):
    # 1. Strip Gutenberg Headers/Footers
    start_pattern = r"\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*"
    match_start = re.search(start_pattern, text)
    if match_start:
        text = text[match_start.end():]

    end_pattern = r"\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*"
    match_end = re.search(end_pattern, text)
    if match_end:
        text = text[:match_end.start()]

    # 2. Specific cleaning based on filename (removing introductions)

    if filename == "the_republic.txt":
        marker = "Socrates, who is the narrator."
        idx = text.find(marker)
        if idx != -1:
            subtext_before = text[:idx]
            republic_marker = "THE REPUBLIC."
            last_republic = subtext_before.rfind(republic_marker)
            if last_republic != -1:
                text = text[last_republic:]
            else:
                text = text[idx:]

    elif filename == "symposium.txt":
        # "SYMPOSIUM"
        # "PERSONS OF THE DIALOGUE"
        # If there is an intro, we want to skip it.
        # Jowett's intros are usually before the text.
        # Let's look for "PERSONS OF THE DIALOGUE" as a safe anchor.
        # But we want the title "SYMPOSIUM" just before it if possible.

        persons_marker = "PERSONS OF THE DIALOGUE"
        idx = text.find(persons_marker)
        if idx != -1:
            # Check if "SYMPOSIUM" is just before it
            sub = text[:idx]
            # Search for "SYMPOSIUM" in the last 200 chars
            last_symp = sub.rfind("SYMPOSIUM")
            if last_symp != -1 and (idx - last_symp) < 500:
                text = text[last_symp:]
            else:
                text = text[idx:]
        else:
            # Fallback
            pass

    elif filename == "apology.txt":
        # Starts with "How you, O Athenians"
        # Let's find that.
        marker = "How you, O Athenians"
        idx = text.find(marker)
        if idx != -1:
            # Maybe include the title if it's close?
            # Title is "Apology" or "APOLOGY"
            sub = text[:idx]
            # Look for "APOLOGY" in the last 1000 chars
            last_title = sub.rfind("APOLOGY")
            if last_title != -1 and (idx - last_title) < 1000:
                # Check if it's the TOC entry?
                # Usually TOC is far away.
                # If we are close, it's likely the header.
                text = text[last_title:]
            else:
                text = text[idx:]

    return text.strip()

def download_and_clean():
    for filename, url in SOURCES.items():
        print(f"Downloading {filename}...")
        response = requests.get(url)
        response.encoding = 'utf-8-sig'
        text = response.text

        print(f"Cleaning {filename}...")
        cleaned_text = clean_text(text, filename)

        # Verify it's not empty
        if len(cleaned_text) < 1000:
            print(f"WARNING: Cleaned text for {filename} seems too short ({len(cleaned_text)} chars). Check markers.")

        filepath = os.path.join(RAW_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Saved to {filepath}")

if __name__ == "__main__":
    download_and_clean()
